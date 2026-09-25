from urllib.parse import urlencode

from aiogram.types import InlineKeyboardButton as B
from aiogram.types import InlineKeyboardMarkup as M

import config
from texts import t


def main_menu(lang: str) -> M:
    return M(inline_keyboard=[
        [B(text=t(lang, "btn_gift"), callback_data="gift"),
         B(text=t(lang, "btn_challenge"), callback_data="challenges")],
        [B(text=t(lang, "btn_profile"), callback_data="profile"),
         B(text=t(lang, "btn_ref"), callback_data="referral")],
        [B(text=t(lang, "btn_support"), callback_data="support"),
         B(text=t(lang, "btn_lang"), callback_data="lang")],
    ])


def back(lang: str, to: str = "menu") -> M:
    return M(inline_keyboard=[[B(text=t(lang, "btn_back"), callback_data=to)]])


def cancel(lang: str) -> M:
    return M(inline_keyboard=[[B(text=t(lang, "btn_cancel"), callback_data="menu")]])


def join(lang: str) -> M:
    rows = []
    if config.CHANNEL_LINK:
        rows.append([B(text=t(lang, "btn_join"), url=config.CHANNEL_LINK)])
    rows.append([B(text=t(lang, "btn_check"), callback_data="check_join")])
    return M(inline_keyboard=rows)


def referral(lang: str, link: str) -> M:
    share_url = "https://t.me/share/url?" + urlencode({"url": link, "text": t(lang, "share_text")})
    return M(inline_keyboard=[
        [B(text=t(lang, "btn_share"), url=share_url)],
        [B(text=t(lang, "btn_back"), callback_data="menu")],
    ])


def challenges(lang: str, items: list[tuple[int, str]]) -> M:
    rows = [[B(text=label, callback_data=f"ch:{cid}")] for cid, label in items]
    rows.append([B(text=t(lang, "btn_refresh"), callback_data="ch_refresh")])
    rows.append([B(text=t(lang, "btn_back"), callback_data="menu")])
    return M(inline_keyboard=rows)


def challenge_detail(lang: str, challenge_id: int, can_join: bool, admin_can_cancel: bool = False) -> M:
    rows = []
    if can_join:
        rows.append([B(text=t(lang, "btn_join_ch"), callback_data=f"chjoin:{challenge_id}")])
    rows.append([B(text=t(lang, "btn_refresh"), callback_data=f"ch:{challenge_id}"),
                 B(text=t(lang, "btn_back_list"), callback_data="challenges")])
    if admin_can_cancel:
        rows.append([B(text=t(lang, "btn_cancel_ch"), callback_data=f"chcancel:{challenge_id}")])
    return M(inline_keyboard=rows)


def languages(lang: str) -> M:
    return M(inline_keyboard=[
        [B(text="🇮🇷 فارسی", callback_data="setlang:fa"),
         B(text="🇬🇧 English", callback_data="setlang:en")],
        [B(text=t(lang, "btn_back"), callback_data="menu")],
    ])
