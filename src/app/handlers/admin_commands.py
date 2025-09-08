from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.app.states.admin import AdminStateSG

admin_commands_router = Router()


@admin_commands_router.message(Command("admin_menu"))
async def send_admin_menu(_, dialog_manager: DialogManager):
    await dialog_manager.start(AdminStateSG.menu)


@admin_commands_router.callback_query(F.data == "back_to_admin_menu")
async def send_admin_menu(_, dialog_manager: DialogManager):
    await dialog_manager.start(AdminStateSG.menu)
