from aiogram.fsm.state import State, StatesGroup


class LoginStates(StatesGroup):
    name = State()
    type = State()
    image = State()
    height = State()
    weight = State()
