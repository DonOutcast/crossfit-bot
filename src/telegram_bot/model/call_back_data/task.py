from aiogram.filters.callback_data import CallbackData


class TaskYesCallBackData(CallbackData, prefix="task_yes_"):
    answer: bool


class TaskNoCallBackData(CallbackData, prefix="task_no_"):
    answer: bool
