from aiogram.fsm.state import State, StatesGroup


class CoordinatesStates(StatesGroup):
    latitude = State()
    longitude = State()
