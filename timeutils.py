import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import config
from texts import t

DB_FMT = "%Y-%m-%d %H:%M:%S"
_DUR = re.compile(r"(\d+)\s*([dhm])")
_MULT = {"d": 86400, "h": 3600, "m": 60}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_db(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime(DB_FMT)


def now_db() -> str:
    return to_db(now_utc())


def from_db(value: str) -> datetime:
    return datetime.strptime(value, DB_FMT).replace(tzinfo=timezone.utc)


def parse_duration(text: str) -> timedelta | None:
    """مثال‌ها: 3d  |  12h  |  90m  |  1d12h  |  2d6h30m"""
    text = (text or "").strip().lower()
    if not text or _DUR.sub("", text).strip():
        return None
    seconds = sum(int(n) * _MULT[u] for n, u in _DUR.findall(text))
    return timedelta(seconds=seconds) if seconds > 0 else None


def is_ended(end_at: str) -> bool:
    return from_db(end_at) <= now_utc()


def remaining(end_at: str, lang: str) -> str:
    secs = int((from_db(end_at) - now_utc()).total_seconds())
    if secs <= 0:
        return t(lang, "ended_short")
    d, r = divmod(secs, 86400)
    h, r = divmod(r, 3600)
    m = r // 60
    parts = [f"{v} {t(lang, k)}" for v, k in ((d, "u_day"), (h, "u_hour"), (m, "u_min")) if v]
    if not parts:
        parts = [f"1 {t(lang, 'u_min')}"]
    return t(lang, "u_and").join(parts[:2])


def _tz():
    try:
        return ZoneInfo(config.TIMEZONE)
    except Exception:
        return timezone.utc


def local_str(end_at: str) -> str:
    return from_db(end_at).astimezone(_tz()).strftime("%Y-%m-%d %H:%M")


def local_now_hm() -> str:
    return now_utc().astimezone(_tz()).strftime("%H:%M")
