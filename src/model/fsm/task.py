from aiogram.fsm.state import State, StatesGroup


class TaskStates(StatesGroup):
    name = State()
    begin = State()
    end = State()
