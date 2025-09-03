from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.app.states.language import ChooseLanguageSG, ChooseTranslateLanguagesSG

language_router = Router()

@language_router.message(Command("language"))
async def setup_language(_, dialog_manager: DialogManager):
    await dialog_manager.start(ChooseLanguageSG.choose_language)


@language_router.message(Command("translate"))
async def setup_language(_, dialog_manager: DialogManager):
    await dialog_manager.start(ChooseTranslateLanguagesSG.choose_language)