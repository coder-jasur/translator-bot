import logging

from asyncpg import Connection

loger = logging.getLogger(__name__)


async def create_database_tables(conn: Connection):
    try:
        await create_users_table(conn)
        await create_channels_table(conn)

    except Exception as e:
        loger.exception(e)


async def create_users_table(conn: Connection):
    query = """ 
        CREATE TABLE IF NOT EXISTS users(
            tg_id BIGINT PRIMARY KEY NOT NULL,
            username TEXT NOT NULL,
            status TEXT NOT NULL,
            language TEXT NOT NULL,
            language_to TEXT,
            language_from TEXT,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """
    await conn.execute(query)


async def create_channels_table(conn: Connection):
    query = """ 
        CREATE TABLE IF NOT EXISTS setup_bot(
            channel_id BIGINT PRIMARY KEY NOT NULL,
            channel_name TEXT NOT NULL,
            channel_username TEXT NOT NULL,
            channel_status TEXT NOT NULL,
            channel_message TEXT,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """
    await conn.execute(query)

