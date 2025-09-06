from aiogram import Router, F, Bot
from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.database.queries.users import UserActions
from src.app.keyboards.inline import not_channels_button
from src.app.states.language import ChooseTranslateLanguagesSG, ChooseLanguageSG
from src.app.texts import texts

check_sub_router = Router()

@check_sub_router.callback_query(F.data == "check_sub")
async def check_channel_sub(
    _,
    dialog_manager: DialogManager,
    conn: Connection,
    bot: Bot,
    lang: str,
):
    channel_actions = ChannelActions(conn)
    user_actions = UserActions(conn)
    user_data = user_actions.get_user(dialog_manager.event.from_user.id)
    channel_data = await channel_actions.get_all_channels()
    not_sub_channels = []

    for channel in channel_data:
        if channel[3] == "True":
            user_status = await bot.get_chat_member(channel[0], dialog_manager.event.from_user.id)
            if user_status.status not in ["member", "administrator", "creator"]:
                not_sub_channels.append(channel)

    if not not_sub_channels:
        if not user_data[3]:
            await dialog_manager.start(ChooseLanguageSG.choose_language)
        else:
            await dialog_manager.start(ChooseTranslateLanguagesSG.choose_language)
    else:
        try:
            await dialog_manager.event.message.edit_text(
                texts["not_subscripted_all_channel"][lang],
                reply_markup=not_channels_button(channel_data),
            )

        except Exception as e:
            print(e)
            await dialog_manager.event.message.edit_text(
                texts["not_subscripted_all_channel"][lang] + ".",
                reply_markup=not_channels_button(channel_data),
            )
