import pytz

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dateutil.relativedelta import relativedelta
from calendar import monthrange

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from model.call_back_data import (
    TimeCallbackDate
)

TIME_ZONE = "Europe/Moscow"
TIME_ZONE_STATIC_TZ = pytz.timezone(TIME_ZONE)

HOURS = {
    "12:00": "🕛",
    "12:30": "🕧",
    "13:00": "🕐",
    "13:30": "🕜",
    "14:00": "🕑",
    "14:30": "🕝",
    "15:00": "🕛",
    "15:30": "🕞",
    "16:00": "🕓",
    "16:30": "🕟",
    "17:00": "🕔",
    "17:30": "🕠",
    "18:00": "🕕",
    "18:30": "🕡",
    "19:00": "🕖",
    "19:30": "🕢",
    "20:00": "🕗",
    "20:30": "🕣",
    "21:00": "🕘",
    "21:30": "🕤",
    "22:00": "🕙",
    "22:30": "🕥",
    "23:00": "🕚",
    "23:30": "🕦",
    "0:00": "🕛",
    "0:30": "🕧",
    "1:00": "🕐",
    "1:30": "🕜",
    "2:00": "🕑",
    "2:30": "🕝",
    "3:00": "🕒",
    "3:30": "🕞",
    "4:00": "🕓",
    "4:30": "🕟",
    "5:00": "🕔",
    "5:30": "🕠",
    "6:00": "🕕",
    "6:30": "🕡",
    "7:00": "🕖",
    "7:30": "🕢",
    "8:00": "🕗",
    "8:30": "🕣",
    "9:00": "🕘",
    "9:30": "🕤",
    "10:00": "🕙",
    "10:30": "🕥",
    "11:00": "🕚",
    "11:30": "🕦",
}


class AioTime:
    pass


def time_until_end_of_day(dt=None):
    import datetime
    kzn_time = datetime.timedelta(hours=0)
    if dt is None:
        dt = datetime.datetime.now() + kzn_time
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min) - dt


def get_time(book_date=None):
    import datetime
    time_menu = InlineKeyboardBuilder()
    if book_date and datetime.datetime.strptime(book_date, "%d/%m/%Y").date() != datetime.datetime.now().date():
        step_count = 48
        finished = datetime.timedelta(days=0)
    else:
        left = time_until_end_of_day()
        time_delta_30_minute = datetime.timedelta(minutes=30)
        step_count = left // time_delta_30_minute
        remainder = left % time_delta_30_minute
        rounded = left - remainder
        finished = datetime.timedelta(days=1) - rounded

    buttons = []
    for i in range(step_count):
        after_split = ':'.join(str(finished).split(':')[:2])

        # if book_date:
        #     call_back_data = f"super_{after_split}_{str(book_date).split(' ')[0]}"
        # else:
        #     call_back_data = f"revers_{after_split}"
        after_split += HOURS.get(after_split, "")
        button = InlineKeyboardButton(text=after_split, callback_data="stump")
        finished += datetime.timedelta(minutes=30)
        buttons.append(button)
        time_menu.button(text=after_split, callback_data="simaple")
    current_count = 4 - len(list(time_menu.buttons)) % 4
    for _ in range(current_count):
        time_menu.button(text=" ", callback_data="⏹")

    time_menu.adjust(4)
    return time_menu.as_markup()
