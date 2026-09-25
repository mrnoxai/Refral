TEXTS: dict[str, dict[str, str]] = {
    "fa": {
        # دکمه‌ها
        "btn_gift": "🎁 کد هدیه",
        "btn_prize": "🏆 جایزه",
        "btn_profile": "👤 پروفایل",
        "btn_ref": "👥 رفرال",
        "btn_support": "💬 پشتیبانی",
        "btn_lang": "🌐 زبان",
        "btn_back": "🔙 بازگشت",
        "btn_cancel": "❌ انصراف",
        "btn_join": "📢 عضویت در کانال",
        "btn_check": "✅ عضو شدم",
        "btn_share": "📤 ارسال لینک برای دوستان",
        "btn_confirm": "✅ تایید و دریافت",
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
        "prizes_title": "🏆 <b>جوایز</b>\n\n🪙 موجودی تو: <b>{tokens}</b> توکن\nیک جایزه را انتخاب کن:",
        "prizes_empty": "🏆 فعلاً جایزه‌ای تعریف نشده است. بعداً سر بزن!",
        "prize_detail": (
            "🏆 <b>{title}</b>\n\n"
            "💰 هزینه: <b>{cost}</b> توکن\n"
            "🪙 موجودی تو: <b>{tokens}</b> توکن\n\n"
            "برای دریافت این جایزه تایید کن:"
        ),
        "prize_ok": (
            "✅ درخواست جایزه «{title}» ثبت شد.\n"
            "🧾 شماره پیگیری: <code>#{claim_id}</code>\n"
            "به‌زودی پشتیبانی با تو در ارتباط خواهد بود."
        ),
        "prize_insufficient": "❌ موجودی توکن کافی نیست.",
        "prize_not_found": "❌ این جایزه دیگر در دسترس نیست.",
        "support_ask": "💬 پیامت را برای پشتیبانی بنویس و ارسال کن (متن، عکس یا فایل):",
        "support_sent": "✅ پیامت برای پشتیبانی ارسال شد. پاسخ از همین ربات برایت می‌آید.",
        "support_reply": "📬 <b>پاسخ پشتیبانی:</b>",
        "lang_choose": "🌐 زبان را انتخاب کن:\nChoose your language:",
        "lang_set": "✅ زبان روی فارسی تنظیم شد.",
        "admin_tokens": "🪙 <b>{amount}</b> توکن توسط مدیریت به حسابت اضافه شد.",
    },
    "en": {
        "btn_gift": "🎁 Gift code",
        "btn_prize": "🏆 Prizes",
        "btn_profile": "👤 Profile",
        "btn_ref": "👥 Referral",
        "btn_support": "💬 Support",
        "btn_lang": "🌐 Language",
        "btn_back": "🔙 Back",
        "btn_cancel": "❌ Cancel",
        "btn_join": "📢 Join channel",
        "btn_check": "✅ I've joined",
        "btn_share": "📤 Share with friends",
        "btn_confirm": "✅ Confirm & claim",
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
        "prizes_title": "🏆 <b>Prizes</b>\n\n🪙 Your balance: <b>{tokens}</b> tokens\nChoose a prize:",
        "prizes_empty": "🏆 No prizes are available right now. Check back later!",
        "prize_detail": (
            "🏆 <b>{title}</b>\n\n"
            "💰 Cost: <b>{cost}</b> tokens\n"
            "🪙 Your balance: <b>{tokens}</b> tokens\n\n"
            "Confirm to claim this prize:"
        ),
        "prize_ok": (
            "✅ Your request for “{title}” has been submitted.\n"
            "🧾 Tracking number: <code>#{claim_id}</code>\n"
            "Support will contact you soon."
        ),
        "prize_insufficient": "❌ Not enough tokens.",
        "prize_not_found": "❌ This prize is no longer available.",
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
