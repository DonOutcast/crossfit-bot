from aiogram.fsm.state import State, StatesGroup


class CurrencyStates(StatesGroup):
    currency = State()
    count = State()
