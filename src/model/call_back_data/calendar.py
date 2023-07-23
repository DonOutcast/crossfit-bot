from aiogram.filters.callback_data import CallbackData


class DateCallbackData(CallbackData, prefix="date_"):
    date: str
    type: str


class TimeCallbackDate(CallbackData, prefix="time"):
    type: str
    time: str
