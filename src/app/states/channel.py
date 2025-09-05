from aiogram.fsm.state import StatesGroup, State

class ChannelsMenu(StatesGroup):
    menu = State()
    add_channel = State()


class ChannelMenu(StatesGroup):
    menu = State()
    delite_channel = State()
    edit_op = State()
    delite_channel_message = State()
    add_channel_message = State()

