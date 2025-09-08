from aiogram import Dispatcher, Router

from src.app.dialogs.user.trasnslate.dialog import  translate_languages
from src.app.dialogs.user.language.dialog import choose_language_dialog


def user_dialog_register(dp: Dispatcher):
    dialog_register_router = Router()

    dialog_register_router.include_router(choose_language_dialog)
    dialog_register_router.include_router(translate_languages)

    dp.include_router(dialog_register_router)