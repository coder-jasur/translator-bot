from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from asyncpg import Connection

from src.app.database.queries.channels import ChannelActions
from src.app.database.queries.users import UserActions


# class CheckSubscription(Filter):
#     async def __call__(self, message: Message | CallbackQuery, conn: Connection, lang: str, **kwargs):
#         channel_actions = ChannelActions(conn)
#         ch = await channel_actions.get_all_channels()

