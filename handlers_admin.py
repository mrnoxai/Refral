import asyncio
import logging
from html import escape

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
import database as db
import challenge_service as svc
from texts import t
from timeutils import local_str, now_utc, parse_duration, remaining, to_db

router = Router()
router.message.filter(F.chat.type == "private", F.from_user.id.in_(config.ADMIN_IDS))
router.callback_query.filter(F.from_user.id.in_(config.ADMIN_IDS))


class CancelState(StatesGroup):
    reason = State()
log = logging.getLogger(__name__)

HELP = (
    "🛠 <b>پنل مدیریت</b>\n\n"
    "<b>آمار</b>\n"
    "/stats — آمار کلی ربات\n"
    "/top — ۱۰ نفر برتر رفرال\n"
    "/user <code>USER_ID</code> — اطلاعات یک کاربر\n\n"
    "<b>توکن</b>\n"
    "/addtokens <code>USER_ID AMOUNT</code> — افزودن/کسر توکن (عدد منفی = کسر)\n\n"
    "<b>کد هدیه</b>\n"
    "/addcode <code>CODE AMOUNT MAX_USES</code> — ساخت کد (MAX_USES=0 یعنی نامحدود)\n"
    "/delcode <code>CODE</code> — حذف کد\n"
    "/codes — لیست کدها\n\n"
    "<b>چالش‌ها</b>\n"
    "/addch <code>مدت [تنظیمات] عنوان | جایزه | توضیحات</code>\n"
    "   مثال ساده: <code>/addch 3d چالش هفته | پریمیوم ۳ ماهه</code>\n"
    "   مثال کامل: <code>/addch 2d winners=3 cost=5 limit=100 cooldown=24 refs=2 چالش ویژه | ۳ پریمیوم | توضیح</code>\n"
    "   مدت: <code>30m</code> دقیقه، <code>12h</code> ساعت، <code>3d</code> روز، ترکیبی <code>1d12h</code>\n"
    "   تنظیمات (همه اختیاری):\n"
    "   • <code>winners=</code> تعداد برنده (پیش‌فرض 1)\n"
    "   • <code>cost=</code> توکن لازم برای شرکت (پیش‌فرض 0 = رایگان)\n"
    "   • <code>limit=</code> ظرفیت شرکت‌کننده (پیش‌فرض 0 = نامحدود)\n"
    f"   • <code>cooldown=</code> برندگان چند ساعت اخیر نتوانند شرکت کنند (پیش‌فرض {config.DEFAULT_WIN_COOLDOWN}، 0 = بدون محدودیت)\n"
    "   • <code>refs=</code> حداقل رفرال لازم (پیش‌فرض 0)\n"
    "/setch <code>ID تنظیمات</code> — تغییر تنظیمات (مثال: <code>/setch 3 winners=2 cooldown=48</code>)\n"
    "/settime <code>ID مدت</code> — تعیین زمان جدید (از الان)\n"
    "/chs — لیست چالش‌ها\n"
    "/parts <code>ID</code> — لیست شرکت‌کنندگان\n"
    "/draw <code>ID</code> — قرعه‌کشی همین الان (بدون صبر تا پایان زمان)\n"
    "/cancelch <code>ID دلیل</code> — لغو چالش + اعلان به کاربران + برگشت هزینه\n"
    "   (یا در صفحه چالش داخل ربات دکمه «🛑 لغو چالش» را بزن)\n"
    "/delch <code>ID</code> — حذف بی‌صدای چالش\n\n"
    "🎲 قرعه‌کشی در پایان زمان هر چالش <b>خودکار</b> انجام می‌شود و به همه شرکت‌کنندگان نتیجه اعلام می‌شود.\n\n"
    "<b>ارسال همگانی</b>\n"
    "روی هر پیامی Reply بزن و بنویس /broadcast\n\n"
    "<b>پشتیبانی</b>\n"
    "برای پاسخ به کاربر، روی پیام پشتیبانی او Reply بزن."
)


@router.message(Command("admin", "help"))
async def cmd_admin(message: Message):
    await message.answer(HELP)


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    s = await db.stats()
    await message.answer(
        "📊 <b>آمار ربات</b>\n\n"
        f"👥 کاربران: <b>{s['users']}</b>\n"
        f"🔗 رفرال‌های موفق: <b>{s['refs']}</b>\n"
        f"🪙 مجموع توکن کاربران: <b>{s['tokens']}</b>\n"
        f"🏆 چالش‌ها: <b>{s['challenges']}</b>\n"
        f"🙋 مجموع شرکت در چالش‌ها: <b>{s['participants']}</b>"
    )


@router.message(Command("top"))
async def cmd_top(message: Message):
    rows = await db.top_referrers(10)
    if not rows:
        await message.answer("هنوز رفرالی ثبت نشده است.")
        return
    lines = ["🏅 <b>برترین‌های رفرال</b>\n"]
    for i, r in enumerate(rows, 1):
        name = escape(r["first_name"] or str(r["user_id"]))
        lines.append(f"{i}. {name} (<code>{r['user_id']}</code>) — {r['ref_count']} رفرال")
    await message.answer("\n".join(lines))


@router.message(Command("user"))
async def cmd_user(message: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if not arg.lstrip("-").isdigit():
        await message.answer("فرمت: /user USER_ID")
        return
    u = await db.get_user(int(arg))
    if not u:
        await message.answer("کاربر پیدا نشد.")
        return
    uname = f"@{u['username']}" if u["username"] else "-"
    await message.answer(
        f"👤 {escape(u['first_name'] or '-')} ({uname})\n"
        f"🆔 <code>{u['user_id']}</code>\n"
        f"🪙 توکن: {u['tokens']}\n"
        f"👥 رفرال: {u['ref_count']}\n"
        f"🔗 معرف: {u['referred_by'] or '-'}\n"
        f"🌐 زبان: {u['lang']}\n"
        f"📅 عضویت: {u['joined_at']}"
    )


@router.message(Command("addtokens"))
async def cmd_addtokens(message: Message, command: CommandObject, bot: Bot):
    parts = (command.args or "").split()
    if len(parts) != 2 or not all(p.lstrip("-").isdigit() for p in parts):
        await message.answer("فرمت: /addtokens USER_ID AMOUNT")
        return
    uid, amount = int(parts[0]), int(parts[1])
    if not await db.add_tokens(uid, amount):
        await message.answer("کاربر پیدا نشد.")
        return
    u = await db.get_user(uid)
    await message.answer(f"✅ انجام شد. موجودی جدید کاربر: {u['tokens']}")
    if amount > 0:
        try:
            await bot.send_message(uid, t(u["lang"], "admin_tokens", amount=amount))
        except Exception:
            pass


@router.message(Command("addcode"))
async def cmd_addcode(message: Message, command: CommandObject):
    parts = (command.args or "").split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        await message.answer("فرمت: /addcode CODE AMOUNT MAX_USES\nمثال: /addcode NOROOZ 5 100")
        return
    code = parts[0].upper()
    await db.add_code(code, int(parts[1]), int(parts[2]))
    limit = "نامحدود" if parts[2] == "0" else parts[2]
    await message.answer(f"✅ کد <code>{escape(code)}</code> ساخته شد — {parts[1]} توکن، ظرفیت: {limit}")


@router.message(Command("delcode"))
async def cmd_delcode(message: Message, command: CommandObject):
    code = (command.args or "").strip().upper()
    if not code:
        await message.answer("فرمت: /delcode CODE")
        return
    ok = await db.del_code(code)
    await message.answer("✅ حذف شد." if ok else "کد پیدا نشد.")


@router.message(Command("codes"))
async def cmd_codes(message: Message):
    rows = await db.list_codes()
    if not rows:
        await message.answer("هیچ کدی وجود ندارد.")
        return
    lines = ["🎁 <b>کدهای هدیه</b>\n"]
    for r in rows:
        limit = "∞" if r["max_uses"] == 0 else r["max_uses"]
        lines.append(f"<code>{escape(r['code'])}</code> — {r['amount']} توکن — استفاده: {r['used_count']}/{limit}")
    await message.answer("\n".join(lines))


# ---------------- چالش‌ها ----------------
OPTION_KEYS = {
    "winners": "winners_count", "برنده": "winners_count",
    "cost": "cost", "هزینه": "cost",
    "limit": "max_participants", "ظرفیت": "max_participants",
    "cooldown": "win_cooldown", "محدودیت": "win_cooldown",
    "refs": "min_refs", "رفرال": "min_refs",
}
STATUS_ICON = {"open": "🟢", "drawing": "🎲", "drawn": "🏁", "cancelled": "🚫"}


def parse_options(tokens: list[str]) -> tuple[dict, int] | None:
    """گزینه‌های key=value ابتدای لیست را می‌خواند. خروجی: (تنظیمات، تعداد توکن مصرف‌شده)"""
    opts, used = {}, 0
    for tok in tokens:
        if "=" not in tok:
            break
        key, _, val = tok.partition("=")
        key = OPTION_KEYS.get(key.strip().lower())
        if not key or not val.strip().isdigit():
            return None
        opts[key] = int(val)
        used += 1
    if "winners_count" in opts and opts["winners_count"] < 1:
        return None
    return opts, used


def settings_text(c) -> str:
    cap = c["max_participants"] or "نامحدود"
    cd = f"{c['win_cooldown']} ساعت" if c["win_cooldown"] else "ندارد"
    return (
        f"🏅 برنده: {c['winners_count']} · 💰 هزینه: {c['cost']} · 👥 ظرفیت: {cap}\n"
        f"⏳ محدودیت برندگان اخیر: {cd} · 🔗 حداقل رفرال: {c['min_refs']}"
    )


@router.message(Command("addch"))
async def cmd_addch(message: Message, command: CommandObject):
    usage = (
        "فرمت: /addch مدت [تنظیمات] عنوان | جایزه | توضیحات\n"
        "مثال: <code>/addch 3d winners=2 چالش هفته | پریمیوم ۳ ماهه | توضیح اختیاری</code>\n"
        "راهنمای کامل: /admin"
    )
    tokens = (command.args or "").split()
    duration = parse_duration(tokens[0]) if tokens else None
    if not duration:
        await message.answer(usage)
        return
    rest = tokens[1:]
    legacy_cost = None
    if rest and rest[0].isdigit():  # سازگاری با فرمت قدیمی: /addch 3d 5 عنوان...
        legacy_cost = int(rest[0])
        rest = rest[1:]
    parsed = parse_options(rest)
    if not parsed:
        await message.answer("❌ تنظیمات نامعتبر است.\n" + usage)
        return
    opts, used = parsed
    fields = [f.strip() for f in " ".join(rest[used:]).split("|")]
    if len(fields) < 2 or not fields[0] or not fields[1]:
        await message.answer(usage)
        return
    if legacy_cost is not None:
        opts.setdefault("cost", legacy_cost)
    opts.setdefault("win_cooldown", config.DEFAULT_WIN_COOLDOWN)
    end_at = to_db(now_utc() + duration)
    cid = await db.add_challenge(fields[0], fields[1], " | ".join(fields[2:]).strip(), end_at, **opts)
    c = await db.get_challenge(cid)
    await message.answer(
        f"✅ چالش #{cid} ساخته شد.\n\n"
        f"🏆 {escape(c['title'])}\n🎁 {escape(c['prize'])}\n"
        f"{settings_text(c)}\n"
        f"⏳ مدت: {remaining(end_at, 'fa')} · 🗓 پایان و قرعه‌کشی: {local_str(end_at)}\n\n"
        "برای اطلاع‌رسانی به کاربران می‌توانی از /broadcast استفاده کنی."
    )


@router.message(Command("setch"))
async def cmd_setch(message: Message, command: CommandObject):
    tokens = (command.args or "").split()
    parsed = parse_options(tokens[1:]) if len(tokens) >= 2 and tokens[0].isdigit() else None
    if not parsed or not parsed[0] or parsed[1] != len(tokens) - 1:
        await message.answer("فرمت: /setch ID تنظیمات\nمثال: <code>/setch 3 winners=2 cooldown=48 limit=50</code>")
        return
    if not await db.update_challenge(int(tokens[0]), parsed[0]):
        await message.answer("چالش پیدا نشد.")
        return
    c = await db.get_challenge(int(tokens[0]))
    await message.answer(f"✅ تنظیمات چالش #{c['id']} به‌روز شد.\n{settings_text(c)}")


@router.message(Command("chs"))
async def cmd_chs(message: Message):
    rows = await db.list_all_challenges()
    if not rows:
        await message.answer("هیچ چالشی وجود ندارد.")
        return
    lines = ["🏆 <b>چالش‌ها</b>  (🟢 باز · 🏁 قرعه‌کشی‌شده · 🚫 لغو‌شده)\n"]
    for c in rows:
        left = remaining(c["end_at"], "fa") if c["status"] == "open" else local_str(c["end_at"])
        lines.append(
            f"{STATUS_ICON.get(c['status'], '')} #{c['id']} — {escape(c['title'])}\n"
            f"   🎁 {escape(c['prize'])} · 👥 {c['cnt']} نفر · 🏅 {c['winners_count']} برنده · ⏳ {left}"
        )
    await message.answer("\n".join(lines))


@router.message(Command("settime"))
async def cmd_settime(message: Message, command: CommandObject):
    parts = (command.args or "").split()
    duration = parse_duration(parts[1]) if len(parts) == 2 else None
    if len(parts) != 2 or not parts[0].isdigit() or not duration:
        await message.answer("فرمت: /settime ID مدت\nمثال: /settime 3 2d")
        return
    end_at = to_db(now_utc() + duration)
    ok = await db.set_challenge_end(int(parts[0]), end_at)
    await message.answer(f"✅ پایان جدید: {local_str(end_at)}" if ok else "چالش باز با این شناسه پیدا نشد.")


@router.message(Command("delch"))
async def cmd_delch(message: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if not arg.isdigit():
        await message.answer("فرمت: /delch ID")
        return
    ok = await db.del_challenge(int(arg))
    await message.answer("✅ چالش حذف شد." if ok else "چالش پیدا نشد.")


@router.message(Command("parts"))
async def cmd_parts(message: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if not arg.isdigit():
        await message.answer("فرمت: /parts ID")
        return
    c = await db.get_challenge(int(arg))
    if not c:
        await message.answer("چالش پیدا نشد.")
        return
    rows = await db.participants(c["id"])
    if not rows:
        await message.answer("هنوز کسی در این چالش شرکت نکرده است.")
        return
    lines = [f"👥 <b>شرکت‌کنندگان چالش #{c['id']}</b> ({len(rows)} نفر)\n"]
    lines += [f"{i}. {svc.user_link(r)}" for i, r in enumerate(rows, 1)]
    if c["status"] == "drawn":
        lines.append("\n🏆 <b>برندگان:</b>")
        lines += [f"• {svc.user_link(w)}" for w in await db.challenge_winners(c["id"])]
    chunk = ""
    for line in lines:
        if len(chunk) + len(line) > 3800:
            await message.answer(chunk)
            chunk = ""
        chunk += line + "\n"
    if chunk:
        await message.answer(chunk)


@router.message(Command("draw"))
async def cmd_draw(message: Message, command: CommandObject, bot: Bot):
    parts = (command.args or "").split()
    if not parts or not parts[0].isdigit() or (len(parts) > 1 and not parts[1].isdigit()):
        await message.answer("فرمت: /draw ID [تعداد برنده]\nمثال: /draw 3")
        return
    count = int(parts[1]) if len(parts) > 1 else None
    await message.answer("🎲 در حال قرعه‌کشی...")
    result = await svc.draw(bot, int(parts[0]), count)
    if result is None:
        await message.answer("❌ چالش باز با این شناسه پیدا نشد (شاید قبلاً قرعه‌کشی یا لغو شده).")


async def _do_cancel(message: Message, bot: Bot, challenge_id: int, reason: str) -> None:
    ok, n = await svc.cancel(bot, challenge_id, reason)
    if ok:
        await message.answer(
            f"🚫 چالش #{challenge_id} لغو شد.\n"
            f"👥 {n} شرکت‌کننده (هزینه شرکت در صورت وجود برگشت داده شد).\n"
            "📨 اعلان لغو در حال ارسال به همه کاربران ربات است..."
        )
    else:
        await message.answer("❌ چالش باز با این شناسه پیدا نشد.")


@router.message(Command("cancelch"))
async def cmd_cancelch(message: Message, command: CommandObject, bot: Bot):
    parts = (command.args or "").split(maxsplit=1)
    if len(parts) != 2 or not parts[0].isdigit():
        await message.answer("فرمت: /cancelch ID دلیل\nمثال: <code>/cancelch 3 مشکل فنی در تأمین جایزه</code>")
        return
    await _do_cancel(message, bot, int(parts[0]), parts[1].strip())


@router.callback_query(F.data.startswith("chcancel:"))
async def cb_cancel_challenge(call: CallbackQuery, state: FSMContext):
    challenge_id = int(call.data.split(":")[1])
    c = await db.get_challenge(challenge_id)
    if not c or c["status"] != "open":
        await call.answer("این چالش قابل لغو نیست.", show_alert=True)
        return
    await state.set_state(CancelState.reason)
    await state.update_data(challenge_id=challenge_id)
    await call.answer()
    await call.message.edit_text(
        f"🛑 لغو چالش #{challenge_id} — {escape(c['title'])}\n\n"
        "✍️ دلیل لغو را بنویس و ارسال کن. این دلیل برای همه کاربران ربات ارسال می‌شود.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ انصراف", callback_data=f"ch:{challenge_id}")]
        ]),
    )


@router.message(CancelState.reason, F.text, ~F.text.startswith("/"))
async def msg_cancel_reason(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()
    await _do_cancel(message, bot, data["challenge_id"], message.text.strip())


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, bot: Bot):
    src = message.reply_to_message
    if not src:
        await message.answer("روی پیامی که می‌خواهی ارسال شود Reply بزن و /broadcast بنویس.")
        return
    ids = await db.all_user_ids()
    status = await message.answer(f"⏳ در حال ارسال به {len(ids)} کاربر...")
    ok = fail = 0
    for uid in ids:
        for _ in range(3):
            try:
                await src.copy_to(uid)
                ok += 1
                break
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except (TelegramForbiddenError, Exception):
                fail += 1
                break
        await asyncio.sleep(0.05)
    await status.edit_text(f"✅ ارسال همگانی تمام شد.\nموفق: {ok}\nناموفق: {fail}")


# ---------------- پاسخ به پشتیبانی ----------------
async def support_target(message: Message):
    reply = message.reply_to_message
    if not reply or (message.text or "").startswith("/"):
        return False
    uid = await db.get_support_user(message.chat.id, reply.message_id)
    return {"target_id": uid} if uid else False


@router.message(support_target)
async def admin_support_reply(message: Message, bot: Bot, target_id: int):
    user = await db.get_user(target_id)
    lang = user["lang"] if user else config.DEFAULT_LANG
    try:
        await bot.send_message(target_id, t(lang, "support_reply"))
        await message.copy_to(target_id)
        await message.reply("✅ پاسخ برای کاربر ارسال شد.")
    except Exception as e:
        await message.reply(f"❌ ارسال نشد: {escape(str(e))}")
