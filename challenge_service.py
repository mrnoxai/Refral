"""منطق چالش‌ها: شرکت، قرعه‌کشی خودکار، لغو و اعلان‌ها."""
import asyncio
import logging
from datetime import timedelta
from html import escape

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter

import config
import database as db
from texts import t
from timeutils import from_db, now_db, now_utc, remaining, to_db

log = logging.getLogger(__name__)
_background: set[asyncio.Task] = set()


# ---------------- ارسال امن پیام ----------------
async def send(bot: Bot, chat_id: int, text: str) -> bool:
    for _ in range(3):
        try:
            await bot.send_message(chat_id, text)
            return True
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except Exception:
            return False
    return False


async def notify_admins(bot: Bot, text: str) -> None:
    for admin_id in config.ADMIN_IDS:
        await send(bot, admin_id, text)


def run_background(coro) -> None:
    task = asyncio.create_task(coro)
    _background.add(task)
    task.add_done_callback(_background.discard)


def user_link(r) -> str:
    uname = f"@{r['username']}" if r["username"] else "-"
    name = escape(r["first_name"] or str(r["user_id"]))
    return f"<a href=\"tg://user?id={r['user_id']}\">{name}</a> ({uname}) <code>{r['user_id']}</code>"


# ---------------- شرکت در چالش ----------------
async def join(challenge_id: int, user) -> tuple[str, dict]:
    """خروجی: (وضعیت، اطلاعات اضافه برای متن پیام)"""
    c = await db.get_challenge(challenge_id)
    if not c or c["status"] == "cancelled":
        return "not_found", {}
    now = now_db()
    if c["status"] != "open" or c["end_at"] <= now:
        return "ended", {}
    if await db.has_joined(challenge_id, user["user_id"]):
        return "already", {}
    if c["min_refs"] and user["ref_count"] < c["min_refs"]:
        return "min_refs", {"n": c["min_refs"], "have": user["ref_count"]}
    if c["win_cooldown"]:
        last = await db.last_win(user["user_id"])
        if last:
            until = from_db(last) + timedelta(hours=c["win_cooldown"])
            if until > now_utc():
                return "cooldown", {"until": to_db(until)}
    status = await db.try_join(challenge_id, user["user_id"], c["cost"], c["max_participants"], now)
    return status, {}


# ---------------- قرعه‌کشی ----------------
async def draw(bot: Bot, challenge_id: int, count: int | None = None):
    """قرعه‌کشی یک چالش. اگر چالش باز نباشد None برمی‌گرداند."""
    if not await db.start_draw(challenge_id):
        return None
    c = await db.get_challenge(challenge_id)
    n = max(count or c["winners_count"] or 1, 1)
    winners = await db.pick_random(challenge_id, n)
    await db.finish_draw(challenge_id, [w["user_id"] for w in winners], now_db())

    everyone = await db.participants(challenge_id)
    win_ids = {w["user_id"] for w in winners}
    title, prize = escape(c["title"]), escape(c["prize"])
    for p in everyone:
        if p["user_id"] in win_ids:
            text = t(p["lang"], "ch_winner", title=title, prize=prize)
        else:
            text = t(p["lang"], "ch_loser", title=title, winners=len(winners), total=len(everyone))
        await send(bot, p["user_id"], text)
        await asyncio.sleep(0.05)

    if winners:
        lines = [
            f"🎲 <b>قرعه‌کشی چالش #{c['id']} انجام شد</b>",
            f"🏆 {title}\n🎁 {prize}",
            f"👥 شرکت‌کنندگان: {len(everyone)} نفر\n",
            "<b>برندگان:</b>",
        ]
        lines += [f"{i}. {user_link(w)}" for i, w in enumerate(winners, 1)]
        lines.append("\n📨 نتیجه برای همه شرکت‌کنندگان ارسال شد.")
    else:
        lines = [f"🎲 چالش #{c['id']} ({title}) تمام شد ولی هیچ شرکت‌کننده‌ای نداشت."]
    await notify_admins(bot, "\n".join(lines))
    return winners


async def scheduler(bot: Bot) -> None:
    """هر ۳۰ ثانیه چالش‌های تمام‌شده را پیدا و قرعه‌کشی می‌کند."""
    while True:
        try:
            for row in await db.due_challenges(now_db()):
                await draw(bot, row["id"])
        except Exception:
            log.exception("Scheduler error")
        await asyncio.sleep(30)


# ---------------- لغو چالش ----------------
async def cancel(bot: Bot, challenge_id: int, reason: str):
    """لغو چالش + برگشت هزینه + اعلان به همه کاربران ربات. خروجی: (موفق؟، تعداد شرکت‌کننده)"""
    c = await db.get_challenge(challenge_id)
    if not c or c["status"] != "open":
        return False, 0
    part_ids = {p["user_id"] for p in await db.participants(challenge_id)}
    if not await db.cancel_challenge(challenge_id, reason):
        return False, 0
    run_background(_announce_cancel(bot, c, reason, part_ids))
    return True, len(part_ids)


async def _announce_cancel(bot: Bot, c, reason: str, part_ids: set[int]) -> None:
    title, reason_html = escape(c["title"]), escape(reason)
    ok = 0
    for u in await db.all_users_lang():
        text = t(u["lang"], "ch_cancelled", title=title, reason=reason_html)
        if u["user_id"] in part_ids and c["cost"] > 0:
            text += t(u["lang"], "ch_refund", n=c["cost"])
        if await send(bot, u["user_id"], text):
            ok += 1
        await asyncio.sleep(0.05)
    await notify_admins(bot, f"📨 اعلان لغو چالش #{c['id']} برای {ok} کاربر ارسال شد.")


def cooldown_left(info: dict, lang: str) -> str:
    return remaining(info["until"], lang)
