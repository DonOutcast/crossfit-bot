from enum import Enum
from typing import List, Optional

import pytz
import calendar
import datetime

import logging.config

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

TIME_ZONE = "Europe/Moscow"
TIME_ZONE_STATIC_TZ = pytz.timezone(TIME_ZONE)


class CalendarAction(str, Enum):
    next_month = "NEXT_MONTH"
    preview_month = "PREVIEW_MONTH"
    next_year = "NEXT_YEAR"
    preview_year = "PREVIEW_YEAR"
    ignore = "IGNORE"
    day = "DAY"
    today = "TODAY"
    selected = "SELECTED"


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
            year: Optional[int] = datetime.datetime.now().year,
            month: Optional[int] = datetime.datetime.now().month,
            all_days: bool = False,
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
            selected_days: Optional[list[datetime.date]] = None,
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
            selected_days=selected_days
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

    @staticmethod
    def _get_date_today() -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text="Teкущая дата",
            callback_data=AioCalendarCallbackData(
                action=CalendarAction.today,
                year=datetime.datetime.today().year,
                month=datetime.datetime.today().month,
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

    def _get_button_with_label(self, label: str, day: int, action: CalendarAction) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=label,
            callback_data=AioCalendarCallbackData(
                action=action,
                year=self.year,
                month=self.month,
                day=day,
            ).pack()
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

    def _create_day_with_current_date(
            self,
            date_now: Optional[datetime.date] = datetime.datetime.now().date(),
            selected_days: Optional[list[datetime.date]] = None
    ):
        line = []
        month_calendar = calendar.monthcalendar(self.year, self.month)
        for week in month_calendar:
            for day in week:
                if not day:
                    line.append(
                        InlineKeyboardButton(
                            text=" ",
                            callback_data=self._get_ignore_callback()
                        )
                    )
                else:
                    current_date_day = datetime.date(self.year, self.month, day)
                    label_day = f"{day}🗓"
                    action = CalendarAction.day
                    if selected_days is not None and current_date_day in selected_days:
                        label_day = f"{day}🔰"
                        action = CalendarAction.selected
                    if current_date_day < date_now:
                        line.append(
                            InlineKeyboardButton(
                                text=label_day,
                                callback_data=self._get_ignore_callback()
                            )
                        )
                    else:
                        line.append(
                            self._get_button_with_label(label_day, day, action)
                        )

        self.builder.row(*line, width=7)

    async def process_selection(
            self,
            query: CallbackQuery,
            data: CallbackData,
            selected_days: Optional[list[datetime.date]] = None
    ) -> tuple[bool, Optional[datetime.date]]:
        result_data = (False, None)
        data = data.dict()
        action = data.get("action")
        if action == CalendarAction.ignore:
            await query.answer(text="Время прошло!", cache_time=30)
        elif action == CalendarAction.next_month:
            temp_date = datetime.datetime(self.year, data.get("month"), 1)
            next_month = temp_date + datetime.timedelta(31)
            self.month = next_month.month
            await query.message.edit_reply_markup(reply_markup=self.get_calendar(selected_days=selected_days))
        elif action == CalendarAction.preview_month:
            temp_date = datetime.datetime(self.year, data.get("month"), 1)
            preview_month = temp_date - datetime.timedelta(1)
            self.month = preview_month.month
            await query.message.edit_reply_markup(reply_markup=self.get_calendar(selected_days=selected_days))
        elif action == CalendarAction.next_year:
            next_year = datetime.datetime(data.get("year") + 1, data.get("month"), 1)
            self.year = next_year.year
            await query.message.edit_reply_markup(reply_markup=self.get_calendar(selected_days=selected_days))
        elif action == CalendarAction.preview_year:
            preview_year = datetime.datetime(data.get("year") - 1, data.get("month"), 1)
            self.year = preview_year.year
            await query.message.edit_reply_markup(reply_markup=self.get_calendar(selected_days=selected_days))
        else:
            await query.message.delete_reply_markup()
            result_data = True, datetime.datetime(int(data.get("year")), int(data.get("month")),
                                                  int(data.get("day"))).date()
        return result_data
