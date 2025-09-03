from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Start, Row
from aiogram_dialog.widgets.text import Const, Format, Case

from src.app.dialogs.admin.handlers import users_count_getter
from src.app.states.admin import AdminStateSG
from src.app.states.broadcast import BroadcasterSG

# admin_menu = Dialog(
#     Window(
#         Const("Выберите действие"),
#         Button(
#             Const("подписки на канал "),
#             id="subscription_channel"
#         ),
#         Start(
#             Const("Рассылка"),
#             id="broadcaster",
#             state=BroadcasterSG.get_creative
#         ),
#         SwitchTo(
#             Const("количества пользывателей"),
#             id="users_count",
#             state=AdminStateSG.users_count
#         ),
#         state=AdminStateSG.menu
#     ),
#     Window(
#         Format("{users_count}"),
#         SwitchTo(Const("назад"), id="back_to_admin_menu", state=AdminStateSG.menu),
#         state=AdminStateSG.users_count,
#         getter=users_count_getter
#     ),
# )

admin_menu = Dialog(
    Window(
        Const("Выберите действие"),
        Start(
            Const("Рассылка"),
            id="broadcaster",
            state=BroadcasterSG.get_creative
        ),
        SwitchTo(
            Const("количества пользывателей"),
            id="users_count",
            state=AdminStateSG.users_count
        ),
        state=AdminStateSG.menu
    ),
    Window(
        Format("{users_count}"),
        SwitchTo(Const("назад"), id="back_to_admin_menu", state=AdminStateSG.menu),
        state=AdminStateSG.users_count,
        getter=users_count_getter
    ),
)



