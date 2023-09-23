from aiogram.fsm.state import State, StatesGroup


class PollStates(StatesGroup):
    question = State()
    answers = State()
    chat_id = State()
