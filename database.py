import os
import sqlite3
from datetime import datetime, timezone

import aiosqlite

import config

_db: aiosqlite.Connection | None = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id      INTEGER PRIMARY KEY,
    username     TEXT,
    first_name   TEXT,
    lang         TEXT    NOT NULL DEFAULT 'fa',
    tokens       INTEGER NOT NULL DEFAULT 0,
    referred_by  INTEGER,
    ref_credited INTEGER NOT NULL DEFAULT 0,
    ref_count    INTEGER NOT NULL DEFAULT 0,
    joined_at    TEXT
);
CREATE TABLE IF NOT EXISTS gift_codes (
    code       TEXT PRIMARY KEY,
    amount     INTEGER NOT NULL,
    max_uses   INTEGER NOT NULL DEFAULT 1,
    used_count INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS code_uses (
    code    TEXT    NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (code, user_id)
);
CREATE TABLE IF NOT EXISTS prizes (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    title  TEXT    NOT NULL,
    cost   INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS claims (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    prize_id   INTEGER NOT NULL,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS challenges (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    prize       TEXT    NOT NULL,
    description TEXT,
    cost        INTEGER NOT NULL DEFAULT 0,
    end_at      TEXT    NOT NULL,
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT
);
CREATE TABLE IF NOT EXISTS participants (
    challenge_id INTEGER NOT NULL,
    user_id      INTEGER NOT NULL,
    joined_at    TEXT,
    PRIMARY KEY (challenge_id, user_id)
);
CREATE TABLE IF NOT EXISTS support_map (
    admin_chat_id INTEGER NOT NULL,
    admin_msg_id  INTEGER NOT NULL,
    user_id       INTEGER NOT NULL,
    PRIMARY KEY (admin_chat_id, admin_msg_id)
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


async def init() -> None:
    global _db
    folder = os.path.dirname(config.DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    _db = await aiosqlite.connect(config.DB_PATH)
    _db.row_factory = aiosqlite.Row
    await _db.execute("PRAGMA journal_mode=WAL")
    await _db.executescript(SCHEMA)
    await _db.commit()


async def close() -> None:
    if _db is not None:
        await _db.close()


async def _one(query: str, *params):
    async with _db.execute(query, params) as cur:
        return await cur.fetchone()


async def _all(query: str, *params):
    async with _db.execute(query, params) as cur:
        return await cur.fetchall()


# ---------------- users ----------------
async def get_user(user_id: int):
    return await _one("SELECT * FROM users WHERE user_id=?", user_id)


async def create_user(user_id, username, first_name, lang, referred_by=None) -> None:
    await _db.execute(
        "INSERT OR IGNORE INTO users(user_id, username, first_name, lang, referred_by, joined_at) "
        "VALUES(?,?,?,?,?,?)",
        (user_id, username, first_name, lang, referred_by, _now()),
    )
    await _db.commit()


async def update_user_info(user_id, username, first_name) -> None:
    await _db.execute(
        "UPDATE users SET username=?, first_name=? WHERE user_id=?", (username, first_name, user_id)
    )
    await _db.commit()


async def set_lang(user_id: int, lang: str) -> None:
    await _db.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
    await _db.commit()


async def add_tokens(user_id: int, amount: int) -> bool:
    cur = await _db.execute("UPDATE users SET tokens=MAX(tokens+?, 0) WHERE user_id=?", (amount, user_id))
    await _db.commit()
    return cur.rowcount == 1


async def credit_referral(user_id: int, reward: int):
    """اگر کاربر رفرال پرداخت‌نشده داشته باشد، به معرف توکن می‌دهد و آیدی معرف را برمی‌گرداند."""
    row = await _one("SELECT referred_by, ref_credited FROM users WHERE user_id=?", user_id)
    if not row or not row["referred_by"] or row["ref_credited"]:
        return None
    cur = await _db.execute(
        "UPDATE users SET ref_credited=1 WHERE user_id=? AND ref_credited=0", (user_id,)
    )
    if cur.rowcount != 1:
        await _db.commit()
        return None
    await _db.execute(
        "UPDATE users SET tokens=tokens+?, ref_count=ref_count+1 WHERE user_id=?",
        (reward, row["referred_by"]),
    )
    await _db.commit()
    return row["referred_by"]


async def all_user_ids() -> list[int]:
    rows = await _all("SELECT user_id FROM users")
    return [r["user_id"] for r in rows]


async def stats() -> dict:
    users = await _one("SELECT COUNT(*) AS c, COALESCE(SUM(tokens),0) AS t FROM users")
    refs = await _one("SELECT COUNT(*) AS c FROM users WHERE ref_credited=1")
    ch = await _one("SELECT COUNT(*) AS c FROM challenges WHERE active=1")
    parts = await _one("SELECT COUNT(*) AS c FROM participants")
    return {"users": users["c"], "tokens": users["t"], "refs": refs["c"],
            "challenges": ch["c"], "participants": parts["c"]}


async def top_referrers(limit: int = 10):
    return await _all(
        "SELECT user_id, first_name, username, ref_count FROM users "
        "WHERE ref_count>0 ORDER BY ref_count DESC LIMIT ?",
        limit,
    )


# ---------------- gift codes ----------------
async def add_code(code: str, amount: int, max_uses: int) -> None:
    await _db.execute(
        "INSERT OR REPLACE INTO gift_codes(code, amount, max_uses, used_count) VALUES(?,?,?,0)",
        (code, amount, max_uses),
    )
    await _db.commit()


async def del_code(code: str) -> bool:
    cur = await _db.execute("DELETE FROM gift_codes WHERE code=?", (code,))
    await _db.commit()
    return cur.rowcount == 1


async def list_codes():
    return await _all("SELECT * FROM gift_codes ORDER BY code")


async def redeem_code(code: str, user_id: int):
    c = await _one("SELECT * FROM gift_codes WHERE code=?", code)
    if not c:
        return "invalid", 0
    if await _one("SELECT 1 FROM code_uses WHERE code=? AND user_id=?", code, user_id):
        return "used", 0
    cur = await _db.execute(
        "UPDATE gift_codes SET used_count=used_count+1 "
        "WHERE code=? AND (max_uses=0 OR used_count<max_uses)",
        (code,),
    )
    if cur.rowcount != 1:
        await _db.commit()
        return "exhausted", 0
    try:
        await _db.execute("INSERT INTO code_uses(code, user_id) VALUES(?,?)", (code, user_id))
    except sqlite3.IntegrityError:
        await _db.rollback()
        return "used", 0
    await _db.execute("UPDATE users SET tokens=tokens+? WHERE user_id=?", (c["amount"], user_id))
    await _db.commit()
    return "ok", c["amount"]


# ---------------- challenges ----------------
_CNT = "(SELECT COUNT(*) FROM participants p WHERE p.challenge_id=c.id) AS cnt"


async def add_challenge(title: str, prize: str, description: str, cost: int, end_at: str) -> int:
    cur = await _db.execute(
        "INSERT INTO challenges(title, prize, description, cost, end_at, created_at) VALUES(?,?,?,?,?,?)",
        (title, prize, description, cost, end_at, _now()),
    )
    await _db.commit()
    return cur.lastrowid


async def del_challenge(challenge_id: int) -> bool:
    cur = await _db.execute("UPDATE challenges SET active=0 WHERE id=? AND active=1", (challenge_id,))
    await _db.commit()
    return cur.rowcount == 1


async def set_challenge_end(challenge_id: int, end_at: str) -> bool:
    cur = await _db.execute("UPDATE challenges SET end_at=? WHERE id=? AND active=1", (end_at, challenge_id))
    await _db.commit()
    return cur.rowcount == 1


async def get_challenge(challenge_id: int):
    return await _one(f"SELECT c.*, {_CNT} FROM challenges c WHERE c.id=? AND c.active=1", challenge_id)


async def list_open_challenges(now: str, user_id: int):
    """چالش‌های فعال و تمام‌نشده + تعداد شرکت‌کننده + اینکه کاربر شرکت کرده یا نه."""
    return await _all(
        f"SELECT c.*, {_CNT}, "
        "EXISTS(SELECT 1 FROM participants p WHERE p.challenge_id=c.id AND p.user_id=?) AS joined "
        "FROM challenges c WHERE c.active=1 AND c.end_at>? ORDER BY c.end_at",
        user_id,
        now,
    )


async def list_all_challenges():
    return await _all(f"SELECT c.*, {_CNT} FROM challenges c WHERE c.active=1 ORDER BY c.id DESC")


async def has_joined(challenge_id: int, user_id: int) -> bool:
    return bool(await _one(
        "SELECT 1 FROM participants WHERE challenge_id=? AND user_id=?", challenge_id, user_id
    ))


async def join_challenge(challenge_id: int, user_id: int, now: str) -> str:
    c = await get_challenge(challenge_id)
    if not c:
        return "not_found"
    if c["end_at"] <= now:
        return "ended"
    if await has_joined(challenge_id, user_id):
        return "already"
    if c["cost"] > 0:
        cur = await _db.execute(
            "UPDATE users SET tokens=tokens-? WHERE user_id=? AND tokens>=?",
            (c["cost"], user_id, c["cost"]),
        )
        if cur.rowcount != 1:
            await _db.commit()
            return "insufficient"
    try:
        await _db.execute(
            "INSERT INTO participants(challenge_id, user_id, joined_at) VALUES(?,?,?)",
            (challenge_id, user_id, _now()),
        )
    except sqlite3.IntegrityError:
        await _db.rollback()
        return "already"
    await _db.commit()
    return "ok"


async def challenge_participants(challenge_id: int):
    return await _all(
        "SELECT u.user_id, u.first_name, u.username, p.joined_at FROM participants p "
        "LEFT JOIN users u ON u.user_id=p.user_id WHERE p.challenge_id=? ORDER BY p.joined_at",
        challenge_id,
    )


async def draw_winners(challenge_id: int, count: int):
    return await _all(
        "SELECT u.user_id, u.first_name, u.username, u.lang FROM participants p "
        "JOIN users u ON u.user_id=p.user_id WHERE p.challenge_id=? ORDER BY RANDOM() LIMIT ?",
        challenge_id,
        count,
    )


# ---------------- support ----------------
async def save_support_map(admin_chat_id: int, admin_msg_id: int, user_id: int) -> None:
    await _db.execute(
        "INSERT OR REPLACE INTO support_map(admin_chat_id, admin_msg_id, user_id) VALUES(?,?,?)",
        (admin_chat_id, admin_msg_id, user_id),
    )
    await _db.commit()


async def get_support_user(admin_chat_id: int, admin_msg_id: int):
    row = await _one(
        "SELECT user_id FROM support_map WHERE admin_chat_id=? AND admin_msg_id=?",
        admin_chat_id,
        admin_msg_id,
    )
    return row["user_id"] if row else None
