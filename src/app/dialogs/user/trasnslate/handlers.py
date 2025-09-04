from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.states.language import ChooseTranslateLanguagesSG
from src.app.texts import texts


async def on_choose_translate_lang_to(
    call: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str
):

    conn: Connection = dialog_manager.middleware_data["conn"]
    user_actions = UserActions(conn)

    if "lang to" in item_id:
        await user_actions.update_user_translate_lang_to(
            item_id.split("_")[0],
            call.from_user.id
        )
    else:
        await user_actions.update_user_translate_lang_from(
            item_id,
            call.from_user.id
        )
    await dialog_manager.switch_to(ChooseTranslateLanguagesSG.choose_language)


async def on_auto_detect(call: CallbackQuery, button: Button, dialog_manager: DialogManager):
    conn: Connection = dialog_manager.middleware_data["conn"]
    lang: str = dialog_manager.middleware_data["lang"]

    user_actions = UserActions(conn)
    try:
        await user_actions.update_user_translate_lang_from(
            button.widget_id,
            call.from_user.id
        )
    except Exception as e:
        print("Error", e)
        await texts["auto_detect"][lang]