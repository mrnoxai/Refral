import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import config
import challenge_service as svc
import database as db
from handlers_admin import router as admin_router
from handlers_user import router as user_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if not config.BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is not set")
    if not config.ADMIN_IDS:
        logging.warning("ADMIN_IDS is empty — support messages and prize requests won't reach anyone.")
    if not config.CHANNEL_ID:
        logging.warning("CHANNEL_ID is empty — channel membership will NOT be checked.")

    await db.init()
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))
    me = await bot.get_me()
    config.BOT_USERNAME = me.username
    logging.info("Bot started as @%s", me.username)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin_router)  # اول ادمین، بعد کاربر
    dp.include_router(user_router)

    await bot.set_my_commands([BotCommand(command="start", description="🏠 منوی اصلی / Main menu")])
    await bot.delete_webhook(drop_pending_updates=True)
    svc.run_background(svc.scheduler(bot))  # قرعه‌کشی خودکار چالش‌ها
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
