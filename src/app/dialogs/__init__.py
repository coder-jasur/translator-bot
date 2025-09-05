from aiogram import Dispatcher, Router

from src.app.dialogs.admin.dialog import admin_menu, OP_dialog, channel_menu_dialog
from src.app.dialogs.user.language.dialog import choose_language_dialog
from src.app.dialogs.user.trasnslate.dialog import translate_languages


def dialog_register(dp: Dispatcher):
    dialog_register_router = Router()

    dialog_register_router.include_router(admin_menu)
    dialog_register_router.include_router(OP_dialog)
    dialog_register_router.include_router(channel_menu_dialog)
    dialog_register_router.include_router(choose_language_dialog)
    dialog_register_router.include_router(translate_languages)

    dp.include_router(dialog_register_router)