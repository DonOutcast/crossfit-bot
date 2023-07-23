from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    name = State()
    image = State()
    height = State()
    weight = State()
    type = State()
