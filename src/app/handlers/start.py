from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.states.language import ChooseTranslateLanguagesSG

start_router = Router()

@start_router.message(CommandStart())
async def start_bot(message: Message, dialog_manager: DialogManager, conn: Connection):
    await dialog_manager.start(ChooseTranslateLanguagesSG.choose_language)






