from typing import AsyncGenerator

from asyncpg import Connection


class UserActions:

    def __init__(self, conn: Connection):
        self._conn = conn

    async def add_user(
        self,
        tg_id: int,
        username: str,
        language: str,
        language_form: str = "auto",
        language_to: str = "ru",
        status: str = "unblocked"
    ):
        query = """
            INSERT INTO users(tg_id, username, status, language, language_from, language_to) VALUES($1, $2, $3, $4, $5, $6 )      
        """
        await self._conn.execute(query, tg_id, username, status, language, language_form, language_to)

    async def get_user(self, tg_id: int):
        query = """
            SELECT * FROM users WHERE tg_id = $1
        """
        return await self._conn.fetchrow(query, tg_id)

    async def get_all_user(self):
        query = """
            SELECT * FROM users 
        """
        return await self._conn.fetch(query)

    async def update_user_status(self, new_status: str, tg_id: int):
        query = """
            UPDATE users SET status = $1 WHERE tg_id = $2
        """
        await self._conn.execute(query, new_status, tg_id)

    async def update_user_lang(self, new_lang: str, tg_id: int):
        query = """
            UPDATE users SET language = $1 WHERE tg_id = $2
        """
        await self._conn.execute(query, new_lang, tg_id)

    async def update_user_translate_lang_to(self, new_lang: str, tg_id: int):
        query = """
            UPDATE users SET language_to = $1 WHERE tg_id = $2
        """
        await self._conn.execute(query, new_lang, tg_id)

    async def update_user_translate_lang_from(self, new_lang: str, tg_id: int):
        query = """
            UPDATE users SET language_from = $1 WHERE tg_id = $2
        """
        await self._conn.execute(query, new_lang, tg_id)

    async def get_user_ids_batch(self, offset: int, limit: int = 5000) -> list[int]:

        query = """
            SELECT tg_id FROM users
            ORDER BY tg_id -- Tartiblash muhim, chunki LIMIT/OFFSET ishonchli ishlashi uchun
            LIMIT $1 OFFSET $2
        """

        rows = await self._conn.fetch(query, limit, offset)

        return [row['tg_id'] for row in rows]

    async def iterate_user_ids(
        self,
        batch_size: int = 5000
    ) -> AsyncGenerator[tuple[list[int], int], None]:

        offset = 0

        while True:
            user_ids = await self.get_user_ids_batch(offset, batch_size)

            if not user_ids:
                break

            yield user_ids, offset
            offset += len(user_ids)
