import logging
from html import escape

from aiogram import Bot, F, Router
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

import config
import database as db
import keyboards as kb
from texts import LANGS, t
import challenge_service as svc
from timeutils import is_ended, local_now_hm, local_str, now_db, remaining

router = Router()
router.message.filter(F.chat.type == "private")
log = logging.getLogger(__name__)


class GiftState(StatesGroup):
    code = State()


class SupportState(StatesGroup):
    message = State()


# ---------------- helpers ----------------
async def is_member(bot: Bot, user_id: int) -> bool:
    if not config.CHANNEL_ID:
        return True
    try:
        m = await bot.get_chat_member(config.CHANNEL_ID, user_id)
    except TelegramBadRequest as e:
        log.error("Membership check failed (is the bot an admin of the channel?): %s", e)
        return False
    if m.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        return True
    return m.status == ChatMemberStatus.RESTRICTED and getattr(m, "is_member", False)


async def safe_edit(call: CallbackQuery, text: str, markup: InlineKeyboardMarkup | None = None) -> None:
    try:
        await call.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        await call.message.answer(text, reply_markup=markup)


async def ensure_user(tg_user):
    user = await db.get_user(tg_user.id)
    if user is None:
        await db.create_user(tg_user.id, tg_user.username, tg_user.full_name, config.DEFAULT_LANG)
        user = await db.get_user(tg_user.id)
    return user


async def guard(call: CallbackQuery, bot: Bot):
    """کاربر را برمی‌گرداند؛ اگر عضو کانال نباشد صفحه عضویت را نشان می‌دهد و None برمی‌گرداند."""
    user = await ensure_user(call.from_user)
    if not await is_member(bot, call.from_user.id):
        await call.answer(t(user["lang"], "not_joined"), show_alert=True)
        await safe_edit(call, t(user["lang"], "must_join"), kb.join(user["lang"]))
        return None
    return user


async def process_referral(bot: Bot, user_id: int) -> None:
    referrer_id = await db.credit_referral(user_id, config.REF_REWARD)
    if not referrer_id:
        return
    ref = await db.get_user(referrer_id)
    if not ref:
        return
    try:
        await bot.send_message(
            referrer_id,
            t(ref["lang"], "new_referral", reward=config.REF_REWARD, tokens=ref["tokens"]),
        )
    except Exception as e:  # کاربر ربات را بلاک کرده و ...
        log.info("Could not notify referrer %s: %s", referrer_id, e)


def ref_link(user_id: int) -> str:
    return f"https://t.me/{config.BOT_USERNAME}?start=ref_{user_id}"


# ---------------- /start ----------------
@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    await state.clear()
    u = message.from_user
    user = await db.get_user(u.id)

    if user is None:
        referrer = None
        arg = (command.args or "").strip()
        if arg.startswith("ref_"):
            arg = arg[4:]
        if arg.isdigit():
            rid = int(arg)
            if rid != u.id and await db.get_user(rid):
                referrer = rid
        await db.create_user(u.id, u.username, u.full_name, config.DEFAULT_LANG, referrer)
        user = await db.get_user(u.id)
    else:
        await db.update_user_info(u.id, u.username, u.full_name)

    lang = user["lang"]
    if not await is_member(bot, u.id):
        await message.answer(t(lang, "must_join"), reply_markup=kb.join(lang))
        return

    await process_referral(bot, u.id)
    await message.answer(
        t(lang, "welcome", name=escape(u.first_name or ""), reward=config.REF_REWARD),
        reply_markup=kb.main_menu(lang),
    )


@router.callback_query(F.data == "check_join")
async def cb_check_join(call: CallbackQuery, bot: Bot):
    user = await ensure_user(call.from_user)
    lang = user["lang"]
    if not await is_member(bot, call.from_user.id):
        await call.answer(t(lang, "not_joined"), show_alert=True)
        return
    await process_referral(bot, call.from_user.id)
    await call.answer()
    await safe_edit(
        call,
        t(lang, "welcome", name=escape(call.from_user.first_name or ""), reward=config.REF_REWARD),
        kb.main_menu(lang),
    )


@router.callback_query(F.data == "menu")
async def cb_menu(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = await guard(call, bot)
    if not user:
        return
    await call.answer()
    await safe_edit(call, t(user["lang"], "main_menu"), kb.main_menu(user["lang"]))


# ---------------- پروفایل ----------------
@router.callback_query(F.data == "profile")
async def cb_profile(call: CallbackQuery, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    lang = user["lang"]
    await call.answer()
    await safe_edit(
        call,
        t(lang, "profile",
          uid=user["user_id"],
          name=escape(call.from_user.full_name),
          tokens=user["tokens"],
          refs=user["ref_count"],
          joined=user["joined_at"] or "-"),
        kb.back(lang),
    )


# ---------------- رفرال ----------------
@router.callback_query(F.data == "referral")
async def cb_referral(call: CallbackQuery, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    lang = user["lang"]
    link = ref_link(user["user_id"])
    await call.answer()
    await safe_edit(
        call,
        t(lang, "referral", reward=config.REF_REWARD, link=link, refs=user["ref_count"], tokens=user["tokens"]),
        kb.referral(lang, link),
    )


# ---------------- کد هدیه ----------------
@router.callback_query(F.data == "gift")
async def cb_gift(call: CallbackQuery, state: FSMContext, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    await state.set_state(GiftState.code)
    await call.answer()
    await safe_edit(call, t(user["lang"], "gift_ask"), kb.cancel(user["lang"]))


@router.message(GiftState.code, F.text)
async def msg_gift_code(message: Message, state: FSMContext):
    user = await ensure_user(message.from_user)
    lang = user["lang"]
    code = message.text.strip().upper()
    status, amount = await db.redeem_code(code, message.from_user.id)
    if status == "ok":
        await state.clear()
        await message.answer(t(lang, "gift_ok", amount=amount), reply_markup=kb.main_menu(lang))
    elif status == "used":
        await state.clear()
        await message.answer(t(lang, "gift_used"), reply_markup=kb.main_menu(lang))
    elif status == "exhausted":
        await state.clear()
        await message.answer(t(lang, "gift_exhausted"), reply_markup=kb.main_menu(lang))
    else:
        await message.answer(t(lang, "gift_invalid"), reply_markup=kb.cancel(lang))


# ---------------- چالش ----------------
def cost_text(lang: str, cost: int) -> str:
    return t(lang, "free") if cost <= 0 else t(lang, "cost_tokens", n=cost)


def count_text(c) -> str:
    return f"{c['cnt']} / {c['max_participants']}" if c["max_participants"] else str(c["cnt"])


async def render_challenges(call: CallbackQuery, user) -> None:
    lang = user["lang"]
    items = await db.list_open_challenges(now_db(), user["user_id"])
    if not items:
        await safe_edit(call, t(lang, "ch_empty", time=local_now_hm()), kb.challenges(lang, []))
        return
    buttons = []
    for c in items:
        mark = "✅ " if c["joined"] else ""
        label = f"{mark}{c['title']} · 👥 {count_text(c)} · ⏳ {remaining(c['end_at'], lang)}"
        buttons.append((c["id"], label))
    await safe_edit(
        call,
        t(lang, "ch_title", tokens=user["tokens"], n=len(items), time=local_now_hm()),
        kb.challenges(lang, buttons),
    )


async def render_challenge(call: CallbackQuery, user, challenge_id: int) -> bool:
    lang = user["lang"]
    c = await db.get_challenge(challenge_id)
    if not c:
        return False
    uid = user["user_id"]
    joined = await db.has_joined(challenge_id, uid)
    is_open = c["status"] == "open" and not is_ended(c["end_at"])

    if c["status"] == "cancelled":
        status = t(lang, "ch_status_cancelled", reason=escape(c["cancel_reason"] or "-"))
    elif c["status"] == "drawn":
        if await db.has_won(challenge_id, uid):
            status = t(lang, "ch_status_won")
        elif joined:
            status = t(lang, "ch_status_lost")
        else:
            status = t(lang, "ch_status_drawn")
    elif not is_open:
        status = t(lang, "ch_status_ended")
    elif joined:
        status = t(lang, "ch_status_joined")
    else:
        status = t(lang, "ch_status_open")

    rules = []
    if c["win_cooldown"]:
        rules.append(t(lang, "rule_cooldown", h=c["win_cooldown"]))
    if c["min_refs"]:
        rules.append(t(lang, "rule_refs", n=c["min_refs"]))
    if c["max_participants"]:
        rules.append(t(lang, "rule_capacity", n=c["max_participants"]))

    text = t(
        lang, "ch_detail",
        title=escape(c["title"]),
        prize=escape(c["prize"]),
        winners=c["winners_count"],
        desc=t(lang, "ch_desc", text=escape(c["description"])) if c["description"] else "",
        count=count_text(c),
        left=remaining(c["end_at"], lang),
        end=local_str(c["end_at"]),
        cost=cost_text(lang, c["cost"]),
        tokens=user["tokens"],
        rules=t(lang, "ch_rules", lines="\n".join(rules)) if rules else "",
        status=status,
    )
    markup = kb.challenge_detail(
        lang, challenge_id,
        can_join=is_open and not joined,
        admin_can_cancel=c["status"] == "open" and uid in config.ADMIN_IDS,
    )
    await safe_edit(call, text, markup)
    return True


@router.callback_query(F.data.in_({"challenges", "ch_refresh"}))
async def cb_challenges(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = await guard(call, bot)
    if not user:
        return
    if call.data == "ch_refresh":
        await call.answer(t(user["lang"], "ch_refreshed"))
    else:
        await call.answer()
    await render_challenges(call, user)


@router.callback_query(F.data.startswith("ch:"))
async def cb_challenge_detail(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    user = await guard(call, bot)
    if not user:
        return
    challenge_id = int(call.data.split(":")[1])
    if await render_challenge(call, user, challenge_id):
        await call.answer()
        return
    await call.answer(t(user["lang"], "ch_not_found"), show_alert=True)
    await render_challenges(call, user)


@router.callback_query(F.data.startswith("chjoin:"))
async def cb_challenge_join(call: CallbackQuery, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    lang = user["lang"]
    challenge_id = int(call.data.split(":")[1])
    status, info = await svc.join(challenge_id, user)
    if status == "min_refs":
        msg = t(lang, "ch_min_refs", **info)
    elif status == "cooldown":
        msg = t(lang, "ch_cooldown", left=svc.cooldown_left(info, lang))
    else:
        msg = t(lang, {
            "ok": "ch_join_ok",
            "already": "ch_already",
            "insufficient": "ch_insufficient",
            "ended": "ch_ended",
            "full": "ch_full",
            "not_found": "ch_not_found",
        }[status])
    await call.answer(msg, show_alert=True)
    user = await db.get_user(user["user_id"])
    if not await render_challenge(call, user, challenge_id):
        await render_challenges(call, user)


# ---------------- پشتیبانی ----------------
@router.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery, state: FSMContext, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    await state.set_state(SupportState.message)
    await call.answer()
    await safe_edit(call, t(user["lang"], "support_ask"), kb.cancel(user["lang"]))


@router.message(SupportState.message)
async def msg_support(message: Message, state: FSMContext, bot: Bot):
    user = await ensure_user(message.from_user)
    lang = user["lang"]
    u = message.from_user
    uname = f"@{u.username}" if u.username else "-"
    header = (
        "📩 <b>پیام پشتیبانی جدید</b>\n"
        f"👤 <a href=\"tg://user?id={u.id}\">{escape(u.full_name)}</a> ({uname})\n"
        f"🆔 <code>{u.id}</code>\n\n"
        "↩️ برای پاسخ، روی همین پیام یا پیام بعدی «Reply» بزن."
    )
    for admin_id in config.ADMIN_IDS:
        try:
            h = await bot.send_message(admin_id, header)
            await db.save_support_map(admin_id, h.message_id, u.id)
            copied = await message.copy_to(admin_id)
            await db.save_support_map(admin_id, copied.message_id, u.id)
        except Exception as e:
            log.warning("Could not forward support message to admin %s: %s", admin_id, e)
    await state.clear()
    await message.answer(t(lang, "support_sent"), reply_markup=kb.main_menu(lang))


# ---------------- زبان ----------------
@router.callback_query(F.data == "lang")
async def cb_lang(call: CallbackQuery, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    await call.answer()
    await safe_edit(call, t(user["lang"], "lang_choose"), kb.languages(user["lang"]))


@router.callback_query(F.data.startswith("setlang:"))
async def cb_set_lang(call: CallbackQuery, bot: Bot):
    user = await guard(call, bot)
    if not user:
        return
    lang = call.data.split(":")[1]
    if lang not in LANGS:
        lang = config.DEFAULT_LANG
    await db.set_lang(call.from_user.id, lang)
    await call.answer(t(lang, "lang_set"))
    await safe_edit(call, t(lang, "main_menu"), kb.main_menu(lang))


# ---------------- پیام‌های دیگر ----------------
@router.message()
async def fallback(message: Message):
    user = await ensure_user(message.from_user)
    await message.answer(t(user["lang"], "main_menu"), reply_markup=kb.main_menu(user["lang"]))
