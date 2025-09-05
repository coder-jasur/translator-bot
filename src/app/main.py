import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs


from logs.logger_conf import setup_logging
from src.app.common.bot_command import bot_commands
from src.app.common.db_url import construct_postgresql_url
from src.app.core.config import Settings
from src.app.database.tables import create_database_tables
from src.app.dialogs import dialog_register
from src.app.handlers import register_all_routers
from src.app.middlewares import register_middlewares

logger = logging.getLogger(__name__)


async def main():
    settings = Settings()

    dsn = construct_postgresql_url(settings)

    pool = await asyncpg.create_pool(
        dsn,
    )
    async with pool.acquire() as conn:
        await create_database_tables(conn)

    dp = Dispatcher()
    register_all_routers(dp, settings.admins_ids)
    register_middlewares(dp, pool, settings)
    setup_dialogs(dp)



    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))

    await bot_commands(bot, settings)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setup_logging("logs/logger.yml")
        asyncio.run(main())
    except Exception as e:
        logger.exception("Closing...", e)
