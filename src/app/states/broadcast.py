

from aiogram.fsm.state import StatesGroup, State


class BroadcasterSG(StatesGroup):
    get_creative = State()
    get_message = State()
    confirm_broadcasting = State()


class BroadcastingManagerSG(StatesGroup):
    start = State()
    get_message = State()
    confirm_broadcasting = State()
