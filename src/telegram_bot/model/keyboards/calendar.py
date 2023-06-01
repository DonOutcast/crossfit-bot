import pytz
from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


class DateCallbackData(CallbackData, prefix="date_"):
    date: str
    type: str


TIME_ZONE = "Europe/Moscow"
TIME_ZONE_STATIC_TZ = pytz.timezone(TIME_ZONE)

if __name__ == "__main__":
    class A:
        name = 1


    def get_name() -> bool:
        return True if getattr(A, "name", None) else False


    print(get_name())
    print(datetime.now())
    print(TIME_ZONE_STATIC_TZ)
    date_now = TIME_ZONE_STATIC_TZ.localize(datetime.now())
    print(date_now.astimezone(TIME_ZONE_STATIC_TZ).strftime("%Y/%m"))


def get_date(date: datetime = None) -> InlineKeyboardMarkup:
    cal_dict = {1: 'Январь',
                2: 'Февраль',
                3: 'Март',
                4: 'Апрель',
                5: 'Май',
                6: 'Июнь',
                7: 'Июль',
                8: 'Август',
                9: 'Сентябрь',
                10: 'Октябрь',
                11: 'Ноябрь',
                12: 'Декабрь'
                }

    date_now = TIME_ZONE_STATIC_TZ.localize(datetime.now())
    date_now.astimezone(TIME_ZONE_STATIC_TZ).strftime("%Y/%m")
    line_year = [
        [
            InlineKeyboardButton(text='⬅️',
                                 callback_data=DateCallbackData(type='refresh',
                                                                date=date_now.strftime("%Y/%m")
                                                                ).pack()
                                 ),
            InlineKeyboardButton(text=date_now.strftime("%Y"),
                                 callback_data=date_now.strftime("%Y")),

            InlineKeyboardButton(text='➡️',
                                 callback_data=DateCallbackData(type='refresh',
                                                                date=date_now.strftime("%Y/%m")
                                                                ).pack()
                                 ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=line_year)
