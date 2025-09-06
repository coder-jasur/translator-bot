from operator import itemgetter

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Start, Row, Select, Group
from aiogram_dialog.widgets.text import Const, Format, Case

from src.app.dialogs.admin.getters import op_menu_getter, add_channel_title_getter, channel_info_getter
from src.app.dialogs.admin.handlers import (
    users_count_getter, add_channel, get_channel_info, on_delete_channel,
    on_edit_op, on_quit_admin_menu, on_broadcast
)
from src.app.states.admin import AdminStateSG
from src.app.states.broadcast import BroadcasterSG
from src.app.states.channel import ChannelsMenu, ChannelMenu

admin_menu = Dialog(
    Window(
        Const("Выберите действие"),
        Start(
            Const("ОП"),
            id="subscription_channel",
            state=ChannelsMenu.menu
        ),
        Button(
            Const("Рассылка"),
            id="broadcaster",
            on_click=on_broadcast
        ),
        SwitchTo(
            Const("количества пользывателей"),
            id="users_count",
            state=AdminStateSG.users_count
        ),
        Button(Const("выйти"), id="quit",  on_click=on_quit_admin_menu),
        state=AdminStateSG.menu
    ),
    Window(
        Format("{users_count}"),
        SwitchTo(Const("назад"), id="back_to_admin_menu", state=AdminStateSG.menu),
        state=AdminStateSG.users_count,
        getter=users_count_getter
    ),
)

OP_dialog = Dialog(
    Window(
        Case(
            {
                "start_msg": Format("Выберите действие"),
                "not_found": Format("вы еще ничего не добавили")
            },
            selector="msg_type"
        ),
        Group(
            Select(
                Format("{item[1]}"),
                id="channels_buttons",
                item_id_getter=itemgetter(0),
                items="channel_data",
                on_click=get_channel_info,

            ),
            width=1
        ),
        SwitchTo(Const("добавить канал"), id="add_channel", state=ChannelsMenu.add_channel),
        Start(Const("назад"), id="back_to_admin_menu", state=AdminStateSG.menu),
        state=ChannelsMenu.menu,
        getter=op_menu_getter
    ),
    Window(
        Case(
            {
                "start_msg": Const("🔗 Чтобы добавить канал или группу..."),
                "not_forwarded": Const("❌ отправьте пост с канала!"),
                "already_exists": Const("уже существует")
            },
            selector="msg_type"
        ),
        MessageInput(func=add_channel, content_types=ContentType.ANY),
        SwitchTo(Const("назад"), id="op_menu", state=ChannelsMenu.menu),
        getter=add_channel_title_getter,
        state=ChannelsMenu.add_channel
    )
)

channel_menu_dialog = Dialog(
    Window(
        Format("{channel_data}"),
        Group(
            Row(
                SwitchTo(Const("❌ Удалить канал"), id="delete_channel", state=ChannelMenu.delite_channel),
                Button(Format("{op_button}"), id="remove_from_op", on_click=on_edit_op),
            ),
            Row(
                Start(Const("⬅️ Назад"), id="back", state=ChannelsMenu.menu),
            ),
        ),
        state=ChannelMenu.menu,
        getter=channel_info_getter
    ),
    Window(
        Const("Вы уверены, что хотите удалить канал?"),
        Row(
            SwitchTo(Const("Нет"), id="back", state=ChannelMenu.menu),
            Button(Const("Да"), id="delete", on_click=on_delete_channel)
        ),
        state=ChannelMenu.delite_channel
    )
)
