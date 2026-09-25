import asyncio
import logging
from html import escape

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import config
import database as db
from texts import t

router = Router()
router.message.filter(F.chat.type == "private", F.from_user.id.in_(config.ADMIN_IDS))
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
    "<b>جوایز</b>\n"
    "/addprize <code>COST TITLE</code> — افزودن جایزه (مثال: /addprize 10 اشتراک یک‌ماهه)\n"
    "/delprize <code>ID</code> — حذف جایزه\n"
    "/prizes — لیست جوایز\n\n"
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
        f"🏆 درخواست‌های جایزه: <b>{s['claims']}</b>"
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


@router.message(Command("addprize"))
async def cmd_addprize(message: Message, command: CommandObject):
    parts = (command.args or "").split(maxsplit=1)
    if len(parts) != 2 or not parts[0].isdigit():
        await message.answer("فرمت: /addprize COST TITLE\nمثال: /addprize 10 اشتراک یک‌ماهه")
        return
    pid = await db.add_prize(parts[1].strip(), int(parts[0]))
    await message.answer(f"✅ جایزه با شناسه {pid} اضافه شد.")


@router.message(Command("delprize"))
async def cmd_delprize(message: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if not arg.isdigit():
        await message.answer("فرمت: /delprize ID")
        return
    ok = await db.del_prize(int(arg))
    await message.answer("✅ حذف شد." if ok else "جایزه پیدا نشد.")


@router.message(Command("prizes"))
async def cmd_prizes(message: Message):
    rows = await db.list_prizes()
    if not rows:
        await message.answer("هیچ جایزه‌ای تعریف نشده است.")
        return
    lines = ["🏆 <b>جوایز</b>\n"]
    for r in rows:
        lines.append(f"#{r['id']} — {escape(r['title'])} — {r['cost']} توکن")
    await message.answer("\n".join(lines))


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
