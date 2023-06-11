from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from model.call_back_data import DateCallbackData
from model.fsm import TaskStates
from model.fsm.login import LoginStates
from model.utils import check_float_value

from model.keyboards import (
    back_to_menu,
    personal_cabinet_keyboard
)
from model.keyboards.calendar import (
    get_date,
    get_time,
    AioCalendar,
    AioCalendarCallbackData,
)
from datetime import datetime

test_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@test_router.message(F.text == "Тест", flags=headers)
async def cmd_tasks(message: Message):
    cal = AioCalendar(datetime.now().year, datetime.now().month)
    cal.all_days = True
    cal.label_preview_month = "⬅️"
    cal.label_next_month = "➡️"
    await message.answer(
        text="🗓 Выберите интересующую вас дату:",
        # reply_markup=get_date(),
        reply_markup=cal.get_calendar()
    )


@test_router.callback_query(AioCalendarCallbackData.filter())
async def catch_calendar(query: CallbackQuery, callback_data: CallbackData) -> None:
    AioCalendar.label_next_month = "➡️"
    AioCalendar.label_preview_month = "⬅️"
    AioCalendar.all_days = True
    result = await AioCalendar(
        callback_data.dict().get("year"),
        callback_data.dict().get("month")
                            ).process_selection(query, callback_data)

@test_router.callback_query(DateCallbackData.filter(F.type == "refresh"))
async def refresh_date(query: CallbackQuery, callback_data: CallbackData) -> None:
    await query.message.edit_reply_markup(
        inline_message_id=query.inline_message_id,
        reply_markup=get_date(datetime.strptime(callback_data.dict().get("date"), "%Y/%m")),
    )


@test_router.callback_query(DateCallbackData.filter(F.type == "get_date"))
async def save_date_get_time(query: CallbackQuery, callback_data: CallbackData) -> None:
    # await query.answer(text="Вы выбрали дату", show_alert=True)
    await query.message.answer(text="Выберите дату")
    await query.message.edit_reply_markup(
        inline_message_id=query.inline_message_id,
        reply_markup=get_time(callback_data.dict().get("date"))
    )
