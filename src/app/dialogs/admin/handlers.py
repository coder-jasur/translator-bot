import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram_dialog import DialogManager, StartMode, Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const, Case
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.database.queries.users import UserActions
from src.app.handlers.broadcasting import start_broadcasting_manager
from src.app.services.broadcaster import Broadcaster
from src.app.states.admin import AdminStateSG
from src.app.states.broadcast import BroadcasterSG, BroadcastingManagerSG
from src.app.states.channel import ChannelsMenu, ChannelMenu

logger = logging.getLogger(__name__)



async def users_count_getter(dialog_manager: DialogManager, **_):
    conn: Connection = dialog_manager.middleware_data["conn"]

    user_actions = UserActions(conn)
    all_users = await user_actions.get_all_user()

    return {"users_count": f"количества пользывателей: {len(all_users)}"}




async def on_broadcast(call: CallbackQuery, __, manager: DialogManager):
    state: FSMContext = manager.middleware_data["state"]
    await manager.done()
    await start_broadcasting_manager(call.message, state)

async def add_channel(message: Message, _, manager: DialogManager) -> None:
    conn: Connection = manager.middleware_data["conn"]

    if not message.forward_from_chat:
        await manager.update({"msg_type": "not_forwarded"})
        return

    try:
        channel_actions = ChannelActions(conn)
        channel_data = await channel_actions.get_channel(message.forward_from_chat.id)
        if channel_data:
            await manager.update({"msg_type": "already_exists"})
            return

        channel_name = message.forward_from_chat.full_name
        channel_id = message.forward_from_chat.id
        channel_username = message.forward_from_chat.username

        await channel_actions.add_channel(channel_id, channel_name, channel_username)
        await manager.switch_to(ChannelsMenu.menu)
        return

    except Exception as e:
        print("Add channel error:", e)


async def get_channel_info(
    _,
    __,
    dialog_manager: DialogManager,
    item_id: str):
    await dialog_manager.start(ChannelMenu.menu, data={"channel_id": int(item_id)})


async def on_delete_channel(_, __, manager: DialogManager):
    conn: Connection = manager.middleware_data["conn"]
    channel_id = manager.dialog_data.get("channel_id")
    channel_actions = ChannelActions(conn)
    print(channel_id)

    await channel_actions.delete_channel(channel_id)
    await manager.switch_to(ChannelsMenu.menu)


async def on_edit_op(_, __, manager: DialogManager):
    conn: Connection = manager.middleware_data["conn"]
    channel_id = manager.dialog_data.get("channel_id")
    channel_actions = ChannelActions(conn)
    channel_data = await channel_actions.get_channel(channel_id)


    if channel_data[3] == "True":
        await channel_actions.update_channel_status("False", channel_id)
        await manager.switch_to(ChannelMenu.menu)
    elif channel_data[3] == "False":
        await channel_actions.update_channel_status("True", channel_id)
        await manager.switch_to(ChannelMenu.menu)


async def on_quit_admin_menu(call: CallbackQuery, __, manager: DialogManager):
    await manager.done()
    await call.message.edit_text("вы вышли из меню админа")



