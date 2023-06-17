from enum import Enum
from typing import List, Optional

import pytz
import calendar
from datetime import datetime, timedelta
import logging.config

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
    DateCallbackData,
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


class CalendarAction(str, Enum):
    next_month = "NEXT_MONTH"
    preview_month = "PREVIEW_MONTH"
    next_year = "NEXT_YEAR"
    preview_year = "PREVIEW_YEAR"
    ignore = "IGNORE"
    day = "DAY"
    today = "TODAY"


class AioCalendarCallbackData(CallbackData, prefix="simple_calendar"):
    action: CalendarAction
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]


class AioCalendar:
    _label_preview_month: str = "<<"
    _label_next_month: str = ">>"
    _label_next_year: str = ">>"
    _label_preview_year: str = "<<"
    _short_names_of_days: list[str] = [
        "Пн",
        "Вт",
        "Ср",
        "Чт",
        "Пт",
        "Сб",
        "Вс",
    ]

    def __init__(
            self,
            year: int,
            month: int,
            all_days: bool = False
    ):
        self._all_days = all_days
        self.builder = InlineKeyboardBuilder()
        self.year = year
        self.month = month

    @classmethod
    def configure(cls, config: dict):
        cls._label_preview_month = config.get('label_preview_month', cls._label_preview_month)
        cls._label_next_month = config.get('label_next_month', cls._label_next_month)
        cls._label_next_year = config.get('label_next_year', cls._label_next_year)
        cls._label_preview_year = config.get('label_preview_year', cls._label_preview_year)
        cls._short_names_of_days = config.get('short_names_of_days', cls._short_names_of_days)

    @property
    def all_days(self) -> bool:
        return self._all_days

    @all_days.setter
    def all_days(self, new_value: bool):
        self._all_days = new_value

    @property
    def short_names_of_days(self) -> list[str]:
        return self._short_names_of_days

    @short_names_of_days.setter
    def short_names_of_days(self, new_names_of_days: list[str]):
        self._short_names_of_days = new_names_of_days

    @property
    def label_next_month(self) -> str:
        return self._label_next_month

    @label_next_month.setter
    def label_next_month(self, new_label: str) -> None:
        self._label_next_month = new_label

    @property
    def label_preview_month(self) -> str:
        return self._label_preview_month

    @label_preview_month.setter
    def label_preview_month(self, new_label: str) -> None:
        self._label_preview_month = new_label

    @property
    def label_next_year(self) -> str:
        return self._label_next_year

    @label_next_year.setter
    def label_next_year(self, new_label: str) -> None:
        self._label_next_year = new_label

    @property
    def label_preview_year(self) -> str:
        return self._label_preview_year

    @label_preview_year.setter
    def label_preview_year(self, new_label: str) -> None:
        self._label_preview_year = new_label

    def get_calendar(
            self,
    ) -> InlineKeyboardMarkup:
        self.builder.row(
            self._get_preview_month(1),
            self._get_label_month_and_year(),
            self._get_next_month(1),
            width=3,
        )
        self.builder.row(
            *self._get_short_names_days(),
            width=7
        )
        self._create_day_with_current_date(
            datetime(
                year=self.year,
                month=self.month,
                day=1
            )
        )
        self.builder.row(
            self._get_preview_year(0),
            self._get_label_year(),
            self._get_next_year(0),
            width=3,
        )
        self.builder.row(
            self._get_date_today(),
            width=1
        )
        return self.builder.as_markup()

    def _get_date_today(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text="Teкущая дата",
            callback_data=AioCalendarCallbackData(
                action=CalendarAction.today,
                year=datetime.today().year,
                month=datetime.today().month,
                day=0,
            ).pack()
        )

    def _get_ignore_callback(self) -> str:
        return AioCalendarCallbackData(
            action=CalendarAction.ignore,
            year=self.year,
            month=self.month,
            day=0,
        ).pack()

    def _get_next_month(self, day) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.label_next_month,
            callback_data=AioCalendarCallbackData(
                action=CalendarAction.next_month,
                year=self.year,
                month=self.month,
                day=day,
            ).pack()
        )

    def _get_preview_month(self, day) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.label_preview_month,
            callback_data=AioCalendarCallbackData(
                action=CalendarAction.preview_month,
                year=self.year,
                month=self.month,
                day=day,
            ).pack()
        )

    def _get_preview_year(self, day: int) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.label_preview_year,
            callback_data=AioCalendarCallbackData(
                action=CalendarAction.preview_year,
                year=self.year,
                month=self.month,
                day=day,
            ).pack()
        )

    def _get_next_year(self, day: int) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.label_next_year,
            callback_data=AioCalendarCallbackData(
                action=CalendarAction.next_year,
                year=self.year,
                month=self.month,
                day=day,
            ).pack()
        )

    def _get_short_names_days(self) -> List[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(
                text=day,
                callback_data=self._get_ignore_callback()
            ) for day in self.short_names_of_days
        ]

    def _get_label_month_and_year(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{calendar.month_name[self.month]} {str(self.year)[2::]}",
            callback_data=self._get_ignore_callback()
        )

    def _get_label_year(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{str(self.year)}",
            callback_data=self._get_ignore_callback()
        )

    def _get_days_of_month(self):
        month_calendar = calendar.monthcalendar(self.year, self.month)
        for week in month_calendar:
            temp = []
            for day in week:
                if day == 0:
                    b = InlineKeyboardButton(
                        text=" ",
                        callback_data=self._get_ignore_callback()
                    )
                    temp.append(b)
                    continue
                b = InlineKeyboardButton(
                    text=str(day),
                    callback_data=AioCalendarCallbackData(
                        action=CalendarAction.day,
                        year=self.year,
                        month=self.month,
                        day=day,
                    ).pack()
                )
                temp.append(b)
            if len(temp) == 7:
                self.builder.row(
                    *temp,
                    width=7)

    def _create_day_with_current_date(self, date: datetime = datetime.now()):
        date_now = TIME_ZONE_STATIC_TZ.localize(date)
        first_day = date_now.weekday()
        count_days = monthrange(date_now.year, date_now.month)[1]
        line = []
        dt_now = datetime.now()
        month_calendar = calendar.monthcalendar(self.year, self.month)
        for number_of_day in range(len(month_calendar) * 7):
            if number_of_day < first_day or number_of_day > count_days + first_day - 1:
                line.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data=self._get_ignore_callback()
                    )
                )
            else:
                day = number_of_day - first_day + 1
                month = date_now.month
                year = date_now.year

                if not self.all_days:
                    if year < dt_now.year or (year == dt_now.year and month < dt_now.month) or (
                            year == dt_now.year and month == dt_now.month and day < dt_now.day):
                        line.append(
                            InlineKeyboardButton(
                                text=" ",
                                callback_data=self._get_ignore_callback()
                            )
                        )
                    else:
                        line.append(
                            InlineKeyboardButton(
                                text=f"{day}🗓",
                                callback_data=AioCalendarCallbackData(
                                    action=CalendarAction.day,
                                    year=self.year,
                                    month=self.month,
                                    day=day,
                                ).pack()
                            )
                        )
                else:
                    line.append(
                        InlineKeyboardButton(
                            text=f"{day}🗓",
                            callback_data=AioCalendarCallbackData(
                                action=CalendarAction.day,
                                year=self.year,
                                month=self.month,
                                day=day,
                            ).pack()
                        )
                    )

            if len(line) == 7:
                self.builder.row(*line, width=7)
                line = []

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple[bool, Optional[datetime]]:
        result_data = (False, None)
        data = data.dict()
        action = data.get("action")
        if action == CalendarAction.ignore:
            await query.answer(cache_time=30)
        elif action == CalendarAction.next_month:
            temp_date = datetime(self.year, data.get("month"), 1)
            next_month = temp_date + timedelta(31)
            self.month = next_month.month
            await query.message.edit_reply_markup(reply_markup=self.get_calendar())
        elif action == CalendarAction.preview_month:
            temp_date = datetime(self.year, data.get("month"), 1)
            preview_month = temp_date - timedelta(1)
            self.month = preview_month.month
            await query.message.edit_reply_markup(reply_markup=self.get_calendar())
        elif action == CalendarAction.next_year:
            next_year = datetime(data.get("year") + 1, data.get("month"), 1)
            self.year = next_year.year
            await query.message.edit_reply_markup(reply_markup=self.get_calendar())
        elif action == CalendarAction.preview_year:
            preview_year = datetime(data.get("year") - 1, data.get("month"), 1)
            self.year = preview_year.year
            await query.message.edit_reply_markup(reply_markup=self.get_calendar())
        else:
            await query.message.delete_reply_markup()
            result_data = True, datetime(int(data.get("year")), int(data.get("month")), int(data.get("day")))
        return result_data


def create_year_buttons(date_now):
    return [
        InlineKeyboardButton(
            text='⬅️',
            callback_data=DateCallbackData(
                type='refresh',
                date=(date_now - relativedelta(years=1)).strftime("%Y/%m")).pack(),
        ),
        InlineKeyboardButton(
            text=date_now.strftime("%Y"),
            callback_data=date_now.strftime("%Y")
        ),
        InlineKeyboardButton(
            text='➡️',
            callback_data=DateCallbackData(
                type='refresh',
                date=(date_now + relativedelta(years=1)).strftime("%Y/%m")).pack()
        )
    ]


def get_days_buttons() -> List[InlineKeyboardButton]:
    days = [
        "Пн",
        "Вт",
        "Ср",
        "Чт",
        "Пт",
        "Сб",
        "Вс"
    ]
    return [InlineKeyboardButton(text=day, callback_data="empty") for day in days]


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
            callback_data=DateCallbackData(
                type='refresh',
                date=(date_now - relativedelta(months=1)).strftime("%Y/%m")).pack(),
        ),
        InlineKeyboardButton(
            text=f"{cal_dict.get(date_now.month)} {date_now.strftime('%Y')}",
            callback_data=date_now.strftime("%m")
        ),
        InlineKeyboardButton(
            text='➡️',
            callback_data=DateCallbackData(
                type='refresh',
                date=(date_now + relativedelta(months=1)).strftime("%Y/%m")).pack()
        )
    ]


def create_day_buttons(date_now, first_day, count_days):
    line = []
    dt_now = datetime.now()

    for number_of_day in range(5 * 7):
        if number_of_day < first_day or number_of_day > count_days + first_day - 1:
            line.append(InlineKeyboardButton(text=' ', callback_data='⏹'))
        else:
            day = number_of_day - first_day + 1
            month = date_now.month
            year = date_now.year

            if year < dt_now.year or (year == dt_now.year and month < dt_now.month) or (
                    year == dt_now.year and month == dt_now.month and day < dt_now.day):
                line.append(InlineKeyboardButton(text=' ', callback_data='⏹'))
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


def get_today_date(date_now: datetime) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text="Сегодня",
            callback_data=DateCallbackData(type='get_date', date=date_now.today().strftime("%d/%m/%y")).pack()
        )
    ]


def get_date(date: datetime = datetime.now()) -> InlineKeyboardMarkup:
    date_now = TIME_ZONE_STATIC_TZ.localize(date)
    # line_year = create_year_buttons(date_now)
    line_days = get_days_buttons()
    line_month = create_month_buttons(date_now)
    line_today = get_today_date(date_now)
    result_inline_keyboard = [
        line_month,
        line_days,
    ]

    first_day = date_now.weekday()
    count_days = monthrange(date_now.year, date_now.month)[1]

    for line in create_day_buttons(date_now, first_day, count_days):
        result_inline_keyboard.append(line)

    # result_inline_keyboard.append(line_year)
    result_inline_keyboard.append(line_today)
    return InlineKeyboardMarkup(inline_keyboard=result_inline_keyboard)


# def get_time(date, start_time=None):
#     # if not start_time:
#     datetime_now = datetime.now()
#     start_hour = datetime_now.hour
#     start_minute = datetime_now.minute
#     if start_minute in range(0, 31):
#         start_time = 30
#     else:
#         start_minute = 0
#         start_hour += 1
#     list_time = []
#     for hour in range(start_hour, 24):
#         for minute in range(start_minute, 60, 30):
#             list_time.append(f"{hour}:{minute:0<2}")
#         start_time = 0
#     if start_time is not None:
#         list_time.append("24 : 00")
#
#     line = []
#     result_list = []
#     flag = False
#     for index, str_time in enumerate(list_time):
#         line.append(
#             InlineKeyboardButton(
#                 text=str_time,
#                 callback_data=TimeCallbackDate(
#                     type="firs" if start_time is None else "last",
#                     date=date,
#                     first_time=str_time if start_time is None else start_time,
#                     last_time=str_time if start_time is not None else ('⏹', '⏹')
#                 ).pack()
#             )
#         )
#         if len(line) == 4:
#             result_list.append(line)
#             line = []
#     result_list.append(line)
#     return InlineKeyboardMarkup(inline_keyboard=result_list)

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
