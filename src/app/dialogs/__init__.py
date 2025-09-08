from aiogram import Dispatcher, Router

from src.app.dialogs.admin.dialog import admin_menu, op_dialog, channel_menu_dialog, add_channel_dialog
from src.app.dialogs.user.trasnslate.dialog import translate_languages


def dialog_register(dp: Dispatcher):
    dialog_register_router = Router()

    dialog_register_router.include_router(admin_menu)
    dialog_register_router.include_router(op_dialog)
    dialog_register_router.include_router(add_channel_dialog)
    dialog_register_router.include_router(channel_menu_dialog)

    dp.include_router(dialog_register_router)

