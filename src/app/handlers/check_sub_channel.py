from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.database.queries.users import UserActions
from src.app.filters.check_channel_sub import CheckSubscription
from src.app.keyboards.inline import not_channels_button
from src.app.texts import texts

check_channel_sub_router = Router()
check_channel_sub_router.message.filter(CheckSubscription())
check_channel_sub_router.callback_query.filter(CheckSubscription())


@check_channel_sub_router.message()
async def check_channel_sub_message(message: Message, conn: Connection, bot: Bot, lang: str):
    channel_actions = ChannelActions(conn)
    channel_data = await channel_actions.get_all_channels()
    not_sub_channels = []
    for channel in channel_data:
        if channel[3] == "True":
            user_status = await bot.get_chat_member(channel[0], message.from_user.id)
            if user_status.status not in ["member", "administrator", "creator"]:
                not_sub_channels.append(channel)

    print(not_sub_channels)

    await message.answer(
        texts["not_subscripted"][lang],
        reply_markup=not_channels_button(not_sub_channels)
    )





@check_channel_sub_router.callback_query()
async def check_channel_sub_call(call: CallbackQuery, conn: Connection, bot: Bot):
    user_actions = UserActions(conn)
    user_data = await user_actions.get_user(call.from_user.id)
    lang = user_data[3]
    channel_actions = ChannelActions(conn)
    channel_data = await channel_actions.get_all_channels()
    not_sub_channels = []
    for channel in channel_data:
        if channel[3] == "True":
            user_status = await bot.get_chat_member(channel[0], call.from_user.id)
            if user_status.status not in ["member", "administrator", "creator"]:
                not_sub_channels.append(channel)

    print(not_sub_channels)

    await call.message.answer(
        texts["not_subscripted"][lang],
        reply_markup=not_channels_button(not_sub_channels)
    )
