import asyncpg
from aiogram import Dispatcher
from aiogram_dialog import DialogManager

from src.app.core.config import Settings
from src.app.middlewares.database_connection import ConnectionMiddleware, PoolMiddleware
from src.app.middlewares.language import LanguageMiddleware
from src.app.middlewares.settings import SettingsMiddleware

def register_middlewares(dp: Dispatcher, pool: asyncpg.pool, settings_: Settings):

    connection_midleware = ConnectionMiddleware(pool)
    dp.message.outer_middleware(connection_midleware)
    dp.callback_query.outer_middleware(connection_midleware)

    language_middleware = LanguageMiddleware()
    dp.message.outer_middleware(language_middleware)
    dp.callback_query.outer_middleware(language_middleware)

    settings_midleware = SettingsMiddleware(settings_)
    dp.message.outer_middleware(settings_midleware)
    dp.callback_query.outer_middleware(settings_midleware)

    pool_middleware = PoolMiddleware(pool)
    dp.message.outer_middleware(pool_middleware)
    dp.callback_query.outer_middleware(pool_middleware)

