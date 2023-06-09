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
from model.keyboards.calendar import get_date, get_time
from datetime import datetime

test_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@test_router.message(F.text == "Тест", flags=headers)
async def cmd_tasks(message: Message):
    await message.answer(
        text="🗓 Выберите интересующую вас дату:",
        reply_markup=get_date(),
    )


@test_router.callback_query(DateCallbackData.filter(F.type == "refresh"))
async def refresh_date(query: CallbackQuery, callback_data: CallbackData) -> None:
    await query.message.edit_reply_markup(
        inline_message_id=query.inline_message_id,
        reply_markup=get_date(datetime.strptime(callback_data.dict().get("date"), "%Y/%m")),
    )


@test_router.callback_query(DateCallbackData.filter(F.type == "get_date"))
async def save_date_get_time(query: CallbackQuery, callback_data: CallbackData) -> None:
    await query.message.answer(text="Выберите дату")
    await query.message.edit_reply_markup(
        inline_message_id=query.inline_message_id,
        reply_markup=get_time(date=callback_data.dict().get("date"))
    )
