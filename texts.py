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
        "btn_cancel_ch": "🛑 لغو چالش (ادمین)",
        # پیام‌ها
        "welcome": (
            "سلام {name} 👋\n"
            "به ربات چالش و رفرال An0nymousteam خوش آمدی!\n\n"
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
            "🏅 تعداد برندگان: <b>{winners}</b> نفر\n"
            "{desc}"
            "👥 شرکت‌کنندگان: <b>{count}</b> نفر\n"
            "⏳ زمان باقی‌مانده: <b>{left}</b>\n"
            "🗓 پایان و قرعه‌کشی: {end}\n"
            "💰 هزینه شرکت: <b>{cost}</b>\n"
            "🪙 موجودی تو: {tokens} توکن\n\n"
            "{rules}"
            "{status}"
        ),
        "ch_desc": "📝 {text}\n",
        "ch_rules": "⚠️ <b>شرایط شرکت:</b>\n{lines}\n\n",
        "rule_cooldown": "• برندگان {h} ساعت اخیر نمی‌توانند شرکت کنند",
        "rule_refs": "• حداقل {n} رفرال موفق لازم است",
        "rule_capacity": "• ظرفیت: {n} نفر",
        "ch_status_open": "👇 برای شرکت در این چالش روی «✅ ثبت شرکت» بزن.",
        "ch_status_joined": "✅ تو در این چالش شرکت کرده‌ای. نتیجه قرعه‌کشی برایت ارسال می‌شود. موفق باشی!",
        "ch_status_ended": "⏳ زمان شرکت تمام شد؛ قرعه‌کشی به‌زودی انجام می‌شود.",
        "ch_status_drawn": "🎲 قرعه‌کشی این چالش انجام شده است.",
        "ch_status_won": "🎲 قرعه‌کشی انجام شد و 🏆 <b>تو برنده این چالش شدی!</b>",
        "ch_status_lost": "🎲 قرعه‌کشی انجام شد؛ این بار برنده نشدی.",
        "ch_status_cancelled": "🚫 این چالش لغو شد.\n📝 دلیل: {reason}",
        "ch_join_ok": "🎉 ثبت شرکت انجام شد! نتیجه قرعه‌کشی بعد از پایان چالش برایت ارسال می‌شود.",
        "ch_already": "✅ قبلاً در این چالش شرکت کرده‌ای.",
        "ch_insufficient": "❌ موجودی توکن برای شرکت در این چالش کافی نیست.",
        "ch_ended": "⛔️ زمان شرکت در این چالش تمام شده است.",
        "ch_not_found": "❌ این چالش دیگر وجود ندارد.",
        "ch_full": "❌ ظرفیت این چالش تکمیل شده است.",
        "ch_min_refs": "❌ برای شرکت در این چالش حداقل {n} رفرال موفق لازم است. (رفرال‌های تو: {have})",
        "ch_cooldown": "⏳ چون اخیراً در یک چالش برنده شده‌ای، فعلاً نمی‌توانی در این چالش شرکت کنی.\nزمان باقی‌مانده: {left}",
        "ch_refreshed": "🔄 بروزرسانی شد",
        "ch_winner": (
            "🎉 <b>تبریک!</b>\n\n"
            "تو در قرعه‌کشی چالش «<b>{title}</b>» برنده شدی! 🏆\n"
            "🎁 جایزه: <b>{prize}</b>\n\n"
            "به‌زودی پشتیبانی برای تحویل جایزه با تو در ارتباط خواهد بود."
        ),
        "ch_loser": (
            "🎲 قرعه‌کشی چالش «<b>{title}</b>» انجام شد.\n\n"
            "😔 متأسفانه این بار برنده نشدی.\n"
            "🏅 تعداد برندگان: {winners} نفر از {total} شرکت‌کننده\n\n"
            "ناامید نشو؛ در چالش‌های بعدی شرکت کن! 💪"
        ),
        "ch_cancelled": (
            "🚫 <b>چالش «{title}» لغو شد.</b>\n\n"
            "📝 دلیل: {reason}"
        ),
        "ch_refund": "\n\n🪙 {n} توکن هزینه شرکت به حسابت برگشت داده شد.",
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
        "btn_cancel_ch": "🛑 Cancel challenge (admin)",
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
            "🏅 Winners: <b>{winners}</b>\n"
            "{desc}"
            "👥 Participants: <b>{count}</b>\n"
            "⏳ Time left: <b>{left}</b>\n"
            "🗓 Ends &amp; draw: {end}\n"
            "💰 Entry cost: <b>{cost}</b>\n"
            "🪙 Your balance: {tokens} tokens\n\n"
            "{rules}"
            "{status}"
        ),
        "ch_desc": "📝 {text}\n",
        "ch_rules": "⚠️ <b>Requirements:</b>\n{lines}\n\n",
        "rule_cooldown": "• Winners from the last {h} hours can't join",
        "rule_refs": "• At least {n} successful referrals required",
        "rule_capacity": "• Capacity: {n} people",
        "ch_status_open": "👇 Tap “✅ Join challenge” to take part.",
        "ch_status_joined": "✅ You have joined this challenge. You'll get the draw result here. Good luck!",
        "ch_status_ended": "⏳ Entry is closed; the draw will happen shortly.",
        "ch_status_drawn": "🎲 The draw for this challenge is done.",
        "ch_status_won": "🎲 The draw is done and 🏆 <b>you won this challenge!</b>",
        "ch_status_lost": "🎲 The draw is done; you didn't win this time.",
        "ch_status_cancelled": "🚫 This challenge was cancelled.\n📝 Reason: {reason}",
        "ch_join_ok": "🎉 You've joined! You'll get the draw result when the challenge ends.",
        "ch_already": "✅ You have already joined this challenge.",
        "ch_insufficient": "❌ You don't have enough tokens to join this challenge.",
        "ch_ended": "⛔️ Entry to this challenge is closed.",
        "ch_not_found": "❌ This challenge no longer exists.",
        "ch_full": "❌ This challenge is full.",
        "ch_min_refs": "❌ You need at least {n} successful referrals to join. (You have {have})",
        "ch_cooldown": "⏳ You won a challenge recently, so you can't join this one yet.\nTime left: {left}",
        "ch_refreshed": "🔄 Refreshed",
        "ch_winner": (
            "🎉 <b>Congratulations!</b>\n\n"
            "You won the draw for “<b>{title}</b>”! 🏆\n"
            "🎁 Prize: <b>{prize}</b>\n\n"
            "Support will contact you soon to deliver your prize."
        ),
        "ch_loser": (
            "🎲 The draw for “<b>{title}</b>” is done.\n\n"
            "😔 Unfortunately you didn't win this time.\n"
            "🏅 Winners: {winners} out of {total} participants\n\n"
            "Don't give up — join the next challenges! 💪"
        ),
        "ch_cancelled": (
            "🚫 <b>The challenge “{title}” has been cancelled.</b>\n\n"
            "📝 Reason: {reason}"
        ),
        "ch_refund": "\n\n🪙 Your {n} token entry fee has been refunded.",
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
