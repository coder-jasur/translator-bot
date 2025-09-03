from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.states.language import ChooseTranslateLanguagesSG


async def on_choose_language(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    conn: Connection = dialog_manager.middleware_data["conn"]
    user_actions = UserActions(conn)
    user_data = await user_actions.get_user(callback.from_user.id)

    if not user_data:
        await user_actions.add_user(
            callback.from_user.id,
            callback.from_user.username or callback.from_user.first_name,
            button.widget_id
        )

    else:
        await user_actions.update_user_lang(button.widget_id, callback.from_user.id)

    await dialog_manager.start(
        ChooseTranslateLanguagesSG.choose_language, mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND, data=str(button.widget_id)
    )