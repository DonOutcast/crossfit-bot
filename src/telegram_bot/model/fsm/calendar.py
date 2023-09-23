from aiogram.fsm.state import State, StatesGroup


class CalendarStates(StatesGroup):
    date = State()
    time = State()
    event = State()
