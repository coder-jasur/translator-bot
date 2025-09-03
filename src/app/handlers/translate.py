from aiogram import Router, F
from aiogram.types import Message
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.services.translators import translate
from src.app.texts import texts

translate_router = Router()

@translate_router.message(F.text)
async def translate_text(message: Message, conn: Connection, lang: str):
    user_actions = UserActions(conn)
    try:
        user_data = await user_actions.get_user(message.from_user.id)
        trasnlated_text = await translate(message.text, user_data[4], user_data[5])
        await message.answer(trasnlated_text)
    except Exception as e:
        print("Error", e)
        await message.answer(texts["error_in_translating"][lang])