from aiogram.filters.callback_data import CallbackData


class ChangePage(CallbackData, prefix="all_currency_"):
    page: int


class CourseCurrency(CallbackData, prefix="course_"):
    name: str
