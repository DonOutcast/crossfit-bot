from aiogram.filters.callback_data import CallbackData


class LoginYesCallBackData(CallbackData, prefix="login_yes_"):
    answer: bool


class LoginNoCallBackData(CallbackData, prefix="login_no_"):
    answer: bool
