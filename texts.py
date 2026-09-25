TEXTS: dict[str, dict[str, str]] = {
    "fa": {
        # دکمه‌ها
        "btn_gift": "🎁 کد هدیه",
        "btn_challenge": "🏆 چالش",
        "btn_profile": "👤 پروفایل",
        "btn_ref": "👥 رفرال",
        "btn_support": "💬 پشتیبانی",
        "btn_lang": "🌐 زبان",
        "btn_back": "🔙 بازگشت",
        "btn_cancel": "❌ انصراف",
        "btn_join": "📢 عضویت در کانال",
        "btn_check": "✅ عضو شدم",
        "btn_share": "📤 ارسال لینک برای دوستان",
        "btn_join_ch": "✅ ثبت شرکت",
        "btn_refresh": "🔄 بروزرسانی",
        "btn_back_list": "🔙 لیست چالش‌ها",
        # پیام‌ها
        "welcome": (
            "سلام {name} 👋\n"
            "به ربات رفرال خوش آمدی!\n\n"
            "🪙 به ازای دعوت هر دوست به کانال، <b>{reward}</b> توکن دریافت می‌کنی.\n"
            "از منوی زیر یک گزینه را انتخاب کن:"
        ),
        "main_menu": "🏠 <b>منوی اصلی</b>\nیک گزینه را انتخاب کن:",
        "must_join": (
            "🔒 برای استفاده از ربات ابتدا باید عضو کانال ما شوی.\n\n"
            "بعد از عضویت روی «✅ عضو شدم» بزن."
        ),
        "not_joined": "❌ هنوز عضو کانال نشده‌ای!",
        "profile": (
            "👤 <b>پروفایل شما</b>\n\n"
            "🆔 شناسه: <code>{uid}</code>\n"
            "👤 نام: {name}\n"
            "🪙 موجودی توکن: <b>{tokens}</b>\n"
            "👥 دعوت‌های موفق: <b>{refs}</b>\n"
            "📅 تاریخ عضویت: {joined}"
        ),
        "referral": (
            "👥 <b>سیستم رفرال</b>\n\n"
            "دوستانت را با لینک اختصاصی زیر دعوت کن. به ازای هر نفر که با لینک تو "
            "وارد ربات و عضو کانال شود، <b>{reward}</b> توکن می‌گیری.\n\n"
            "🔗 لینک تو:\n<code>{link}</code>\n\n"
            "👥 دعوت‌های موفق: <b>{refs}</b>\n"
            "🪙 موجودی: <b>{tokens}</b>"
        ),
        "share_text": "🎁 با این لینک عضو شو و جایزه بگیر!",
        "new_referral": (
            "🎉 یک نفر با لینک تو عضو شد!\n"
            "🪙 <b>{reward}</b> توکن به حسابت اضافه شد.\n"
            "موجودی فعلی: <b>{tokens}</b>"
        ),
        "gift_ask": "🎁 کد هدیه‌ات را ارسال کن:",
        "gift_ok": "✅ کد هدیه ثبت شد!\n🪙 <b>{amount}</b> توکن به حسابت اضافه شد.",
        "gift_invalid": "❌ این کد معتبر نیست. دوباره امتحان کن یا انصراف بده.",
        "gift_used": "⚠️ قبلاً از این کد استفاده کرده‌ای.",
        "gift_exhausted": "⌛️ ظرفیت استفاده از این کد تمام شده است.",
        "ch_title": (
            "🏆 <b>چالش‌ها و جوایز</b>\n\n"
            "🪙 موجودی تو: <b>{tokens}</b> توکن\n"
            "📋 چالش‌های فعال: <b>{n}</b>\n\n"
            "روی هر چالش بزن تا جزئیات را ببینی و شرکت کنی.\n"
            "✅ = چالش‌هایی که در آن شرکت کرده‌ای\n\n"
            "🕒 آخرین بروزرسانی: {time}"
        ),
        "ch_empty": (
            "🏆 فعلاً چالش فعالی وجود ندارد.\n"
            "با دکمه «🔄 بروزرسانی» دوباره بررسی کن.\n\n"
            "🕒 آخرین بروزرسانی: {time}"
        ),
        "ch_detail": (
            "🏆 <b>{title}</b>\n\n"
            "🎁 جایزه: <b>{prize}</b>\n"
            "{desc}"
            "👥 تعداد شرکت‌کنندگان: <b>{count}</b> نفر\n"
            "⏳ زمان باقی‌مانده: <b>{left}</b>\n"
            "🗓 پایان: {end}\n"
            "💰 هزینه شرکت: <b>{cost}</b>\n"
            "🪙 موجودی تو: {tokens} توکن\n\n"
            "{status}"
        ),
        "ch_desc": "📝 {text}\n\n",
        "ch_status_open": "👇 برای شرکت در این چالش روی «✅ ثبت شرکت» بزن.",
        "ch_status_joined": "✅ تو در این چالش شرکت کرده‌ای. موفق باشی!",
        "ch_status_ended": "⛔️ زمان شرکت در این چالش تمام شده است.",
        "ch_join_ok": "🎉 ثبت شرکت انجام شد! با موفقیت در چالش شرکت کردی.",
        "ch_already": "✅ قبلاً در این چالش شرکت کرده‌ای.",
        "ch_insufficient": "❌ موجودی توکن برای شرکت در این چالش کافی نیست.",
        "ch_ended": "⛔️ زمان این چالش تمام شده است.",
        "ch_not_found": "❌ این چالش دیگر وجود ندارد.",
        "ch_refreshed": "🔄 بروزرسانی شد",
        "ch_winner": (
            "🎉 <b>تبریک!</b>\n\n"
            "تو برنده چالش «{title}» شدی! 🏆\n"
            "🎁 جایزه: <b>{prize}</b>\n\n"
            "به‌زودی پشتیبانی برای تحویل جایزه با تو در ارتباط خواهد بود."
        ),
        "free": "رایگان",
        "cost_tokens": "{n} توکن",
        "ended_short": "پایان یافته",
        "u_day": "روز",
        "u_hour": "ساعت",
        "u_min": "دقیقه",
        "u_and": " و ",
        "support_ask": "💬 پیامت را برای پشتیبانی بنویس و ارسال کن (متن، عکس یا فایل):",
        "support_sent": "✅ پیامت برای پشتیبانی ارسال شد. پاسخ از همین ربات برایت می‌آید.",
        "support_reply": "📬 <b>پاسخ پشتیبانی:</b>",
        "lang_choose": "🌐 زبان را انتخاب کن:\nChoose your language:",
        "lang_set": "✅ زبان روی فارسی تنظیم شد.",
        "admin_tokens": "🪙 <b>{amount}</b> توکن توسط مدیریت به حسابت اضافه شد.",
    },
    "en": {
        "btn_gift": "🎁 Gift code",
        "btn_challenge": "🏆 Challenges",
        "btn_profile": "👤 Profile",
        "btn_ref": "👥 Referral",
        "btn_support": "💬 Support",
        "btn_lang": "🌐 Language",
        "btn_back": "🔙 Back",
        "btn_cancel": "❌ Cancel",
        "btn_join": "📢 Join channel",
        "btn_check": "✅ I've joined",
        "btn_share": "📤 Share with friends",
        "btn_join_ch": "✅ Join challenge",
        "btn_refresh": "🔄 Refresh",
        "btn_back_list": "🔙 Challenges",
        "welcome": (
            "Hi {name} 👋\n"
            "Welcome to the referral bot!\n\n"
            "🪙 You get <b>{reward}</b> token(s) for every friend you invite to the channel.\n"
            "Choose an option below:"
        ),
        "main_menu": "🏠 <b>Main menu</b>\nChoose an option:",
        "must_join": (
            "🔒 To use this bot, please join our channel first.\n\n"
            "After joining, tap “✅ I've joined”."
        ),
        "not_joined": "❌ You haven't joined the channel yet!",
        "profile": (
            "👤 <b>Your profile</b>\n\n"
            "🆔 ID: <code>{uid}</code>\n"
            "👤 Name: {name}\n"
            "🪙 Tokens: <b>{tokens}</b>\n"
            "👥 Successful referrals: <b>{refs}</b>\n"
            "📅 Joined: {joined}"
        ),
        "referral": (
            "👥 <b>Referral program</b>\n\n"
            "Invite friends with your personal link. For each person who starts the bot "
            "with your link and joins the channel, you get <b>{reward}</b> token(s).\n\n"
            "🔗 Your link:\n<code>{link}</code>\n\n"
            "👥 Successful referrals: <b>{refs}</b>\n"
            "🪙 Balance: <b>{tokens}</b>"
        ),
        "share_text": "🎁 Join with this link and win prizes!",
        "new_referral": (
            "🎉 Someone joined with your link!\n"
            "🪙 <b>{reward}</b> token(s) added to your balance.\n"
            "Current balance: <b>{tokens}</b>"
        ),
        "gift_ask": "🎁 Send your gift code:",
        "gift_ok": "✅ Gift code redeemed!\n🪙 <b>{amount}</b> token(s) added to your balance.",
        "gift_invalid": "❌ This code is not valid. Try again or cancel.",
        "gift_used": "⚠️ You have already used this code.",
        "gift_exhausted": "⌛️ This code has reached its usage limit.",
        "ch_title": (
            "🏆 <b>Challenges &amp; prizes</b>\n\n"
            "🪙 Your balance: <b>{tokens}</b> tokens\n"
            "📋 Active challenges: <b>{n}</b>\n\n"
            "Tap a challenge to see details and join.\n"
            "✅ = challenges you have joined\n\n"
            "🕒 Last updated: {time}"
        ),
        "ch_empty": (
            "🏆 There are no active challenges right now.\n"
            "Tap “🔄 Refresh” to check again.\n\n"
            "🕒 Last updated: {time}"
        ),
        "ch_detail": (
            "🏆 <b>{title}</b>\n\n"
            "🎁 Prize: <b>{prize}</b>\n"
            "{desc}"
            "👥 Participants: <b>{count}</b>\n"
            "⏳ Time left: <b>{left}</b>\n"
            "🗓 Ends: {end}\n"
            "💰 Entry cost: <b>{cost}</b>\n"
            "🪙 Your balance: {tokens} tokens\n\n"
            "{status}"
        ),
        "ch_desc": "📝 {text}\n\n",
        "ch_status_open": "👇 Tap “✅ Join challenge” to take part.",
        "ch_status_joined": "✅ You have joined this challenge. Good luck!",
        "ch_status_ended": "⛔️ This challenge is closed.",
        "ch_join_ok": "🎉 You have successfully joined the challenge!",
        "ch_already": "✅ You have already joined this challenge.",
        "ch_insufficient": "❌ You don't have enough tokens to join this challenge.",
        "ch_ended": "⛔️ This challenge has ended.",
        "ch_not_found": "❌ This challenge no longer exists.",
        "ch_refreshed": "🔄 Refreshed",
        "ch_winner": (
            "🎉 <b>Congratulations!</b>\n\n"
            "You won the challenge “{title}”! 🏆\n"
            "🎁 Prize: <b>{prize}</b>\n\n"
            "Support will contact you soon to deliver your prize."
        ),
        "free": "Free",
        "cost_tokens": "{n} tokens",
        "ended_short": "Ended",
        "u_day": "d",
        "u_hour": "h",
        "u_min": "min",
        "u_and": " ",
        "support_ask": "💬 Write your message to support and send it (text, photo or file):",
        "support_sent": "✅ Your message was sent to support. You'll get the reply here.",
        "support_reply": "📬 <b>Support reply:</b>",
        "lang_choose": "🌐 زبان را انتخاب کن:\nChoose your language:",
        "lang_set": "✅ Language set to English.",
        "admin_tokens": "🪙 <b>{amount}</b> token(s) were added to your balance by the admin.",
    },
}

LANGS = tuple(TEXTS.keys())


def t(lang: str, key: str, **kwargs) -> str:
    table = TEXTS.get(lang) or TEXTS["fa"]
    text = table.get(key) or TEXTS["fa"][key]
    return text.format(**kwargs) if kwargs else text
