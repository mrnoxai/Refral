import os

from dotenv import load_dotenv

load_dotenv()


def _parse_ids(value: str) -> list[int]:
    return [int(x) for x in value.replace(" ", "").split(",") if x.strip().lstrip("-").isdigit()]


def _parse_chat(value: str):
    value = value.strip()
    if value.lstrip("-").isdigit():
        return int(value)
    if value and not value.startswith("@"):
        value = "@" + value
    return value


BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS: list[int] = _parse_ids(os.getenv("ADMIN_IDS", ""))

# @channel_username  یا  -100xxxxxxxxxx (برای کانال خصوصی)
CHANNEL_ID = _parse_chat(os.getenv("CHANNEL_ID", ""))
# لینک عضویت کانال (برای کانال خصوصی حتماً پر شود)
CHANNEL_LINK: str = os.getenv("CHANNEL_LINK", "").strip()
if not CHANNEL_LINK and isinstance(CHANNEL_ID, str) and CHANNEL_ID.startswith("@"):
    CHANNEL_LINK = f"https://t.me/{CHANNEL_ID[1:]}"

# تعداد توکن به ازای هر رفرال موفق
REF_REWARD: int = int(os.getenv("REF_REWARD", "1"))
DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "fa").strip() or "fa"
DB_PATH: str = os.getenv("DB_PATH", "data/bot.db").strip()

# در زمان اجرا مقداردهی می‌شود
BOT_USERNAME: str = ""
