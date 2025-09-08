from aiogram.fsm.state import StatesGroup, State


class AdminStateSG(StatesGroup):
    menu = State()
    users_count = State()

