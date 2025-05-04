import asyncio, logging
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config.config import TOKEN
from states.dispatcher import dp
from handlers.driver import driver
from handlers.user import main_user_handler, tech_support, application, error_handler, cabinet

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(driver.router)
    dp.include_router(main_user_handler.router)
    dp.include_router(cabinet.router)
    dp.include_router(tech_support.router)
    dp.include_router(application.router)
    dp.include_routers(error_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())