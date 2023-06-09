from aiogram.filters.callback_data import CallbackData


class DateCallbackData(CallbackData, prefix="date_"):
    date: str
    type: str


class TimeCallbackDate(CallbackData, prefix="time"):
    type: str
    date: str
    first_time: str
    last_time: str
