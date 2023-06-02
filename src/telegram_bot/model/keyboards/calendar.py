import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange

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


# def get_date(date: datetime = datetime.now()) -> InlineKeyboardMarkup:
#     cal_dict = {1: 'Январь',
#                 2: 'Февраль',
#                 3: 'Март',
#                 4: 'Апрель',
#                 5: 'Май',
#                 6: 'Июнь',
#                 7: 'Июль',
#                 8: 'Август',
#                 9: 'Сентябрь',
#                 10: 'Октябрь',
#                 11: 'Ноябрь',
#                 12: 'Декабрь'
#                 }
#
#
#     date_now = TIME_ZONE_STATIC_TZ.localize(date)
#     date_now.astimezone(TIME_ZONE_STATIC_TZ).strftime("%Y/%m")
#     line_year = [
#
#         InlineKeyboardButton(
#             text='⬅️',
#             callback_data=DateCallbackData(type='refresh',
#                                            date=date_now.strftime("%Y/%m")).pack()
#         ),
#         InlineKeyboardButton(
#             text=date_now.strftime("%Y"),
#             callback_data=date_now.strftime("%Y")
#         ),
#
#         InlineKeyboardButton(
#             text='➡️',
#             callback_data=DateCallbackData(type='refresh',
#                                            date=date_now.strftime("%Y/%m")
#                                            ).pack()
#         ),
#
#     ]
#     line_month = [
#
#         InlineKeyboardButton(
#             text='⬅️',
#             callback_data=DateCallbackData(
#                 type="refresh",
#                 date=(date_now.strftime("%Y/%m"))
#             ).pack()
#         ),
#         InlineKeyboardButton(
#             text=cal_dict.get(date_now.month),
#             callback_data=date_now.strftime("%m")
#         ),
#         InlineKeyboardButton(
#             text='➡️',
#             callback_data=DateCallbackData(
#                 type="refresh",
#                 date=(date_now.strftime("%Y/%m"))
#             ).pack()
#         )
#
#     ]
#     result_inline_keyboard = [line_month, ]
#
#     first_day = date_now.weekday()
#     count_days = monthrange(date_now.year, date_now.month)[1]
#     dt_now = datetime.now()
#
#     line = []
#     for number_of_day in range(6 * 6):
#         if number_of_day < first_day or number_of_day > count_days + first_day - 1:
#             line.append(
#                 InlineKeyboardButton(
#                     text='_', callback_data='_'
#                 )
#             )
#         else:
#
#             day = number_of_day - first_day + 1
#             mount = date_now.month
#             year = date_now.year
#
#             if year < dt_now.year:
#                 line.append(
#                     InlineKeyboardButton(
#                         text='_', callback_data='_'
#                     )
#                 )
#             if year > dt_now.year:
#                 line.append(
#                     InlineKeyboardButton(
#                         text=str(day),
#                         callback_data=DateCallbackData(
#                             type='get_date',
#                             date=f'{day}/{mount}/{year}').pack()
#                     )
#                 )
#             else:
#                 if mount < dt_now.month:
#                     line.append(
#                         InlineKeyboardButton(
#                             text='_',
#                             callback_data='_'
#                         )
#                     )
#                 if mount > dt_now.month:
#                     line.append(
#                         InlineKeyboardButton(
#                             text=str(day),
#                             callback_data=DateCallbackData(
#                                 type='get_date',
#                                 date=f'{day}/{mount}/{year}').pack()
#                         )
#                     )
#                 else:
#                     if day < dt_now.day:
#                         line.append(
#                             InlineKeyboardButton(
#                                 text='_',
#                                 callback_data='_'
#                             )
#                         )
#                     else:
#                         line.append(
#                             InlineKeyboardButton(
#                                 text=str(day),
#                                 callback_data=DateCallbackData(
#                                     type='get_date',
#                                     date=f'{day}/{mount}/{year}').pack()
#                             )
#                         )
#
#         if len(line) == 7:
#             result_inline_keyboard.append(line)
#             line = []
#
#     result_inline_keyboard.append(line_year)
#
#     return InlineKeyboardMarkup(
#         inline_keyboard=result_inline_keyboard
#     )

def create_year_buttons(date_now):
    return [
        InlineKeyboardButton(
            text='⬅️',
            callback_data=DateCallbackData(type='refresh', date=date_now.strftime("%Y/%m")).pack()
        ),
        InlineKeyboardButton(
            text=date_now.strftime("%Y"),
            callback_data=date_now.strftime("%Y")
        ),
        InlineKeyboardButton(
            text='➡️',
            callback_data=DateCallbackData(type='refresh', date=date_now.strftime("%Y/%m")).pack()
        )
    ]


def create_month_buttons(date_now):
    cal_dict = {
        1: 'Январь',
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

    return [
        InlineKeyboardButton(
            text='⬅️',
            callback_data=DateCallbackData(type='refresh', date=date_now.strftime("%Y/%m")).pack()
        ),
        InlineKeyboardButton(
            text=cal_dict.get(date_now.month),
            callback_data=date_now.strftime("%m")
        ),
        InlineKeyboardButton(
            text='➡️',
            callback_data=DateCallbackData(type='refresh', date=date_now.strftime("%Y/%m")).pack()
        )
    ]


def create_day_buttons(date_now, first_day, count_days):
    line = []
    dt_now = datetime.now()

    for number_of_day in range(5 * 7):
        if number_of_day < first_day or number_of_day > count_days + first_day - 1:
            line.append(InlineKeyboardButton(text='⏹', callback_data='⏹'))
        else:
            day = number_of_day - first_day + 1
            month = date_now.month
            year = date_now.year

            if year < dt_now.year or (year == dt_now.year and month < dt_now.month) or (
                    year == dt_now.year and month == dt_now.month and day < dt_now.day):
                line.append(InlineKeyboardButton(text='⏹', callback_data='⏹'))
            else:
                line.append(
                    InlineKeyboardButton(
                        text=str(day),
                        callback_data=DateCallbackData(type='get_date', date=f'{day}/{month}/{year}').pack()
                    )
                )

        if len(line) == 7:
            yield line
            line = []


def get_date(date: datetime = datetime.now()) -> InlineKeyboardMarkup:
    date_now = TIME_ZONE_STATIC_TZ.localize(date)
    line_year = create_year_buttons(date_now)
    line_month = create_month_buttons(date_now)
    result_inline_keyboard = [line_month]

    first_day = date_now.weekday()
    count_days = monthrange(date_now.year, date_now.month)[1]

    for line in create_day_buttons(date_now, first_day, count_days):
        result_inline_keyboard.append(line)

    result_inline_keyboard.append(line_year)

    return InlineKeyboardMarkup(inline_keyboard=result_inline_keyboard)
