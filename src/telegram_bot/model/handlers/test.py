from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession

from model.fsm.login import LoginStates
from model.utils import check_float_value

from model.keyboards import (
    back_to_menu,
    personal_cabinet_keyboard
)
from model.keyboards.calendar import get_date

test_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@test_router.message(F.text == "Тест", flags=headers)
async def cmd_tasks(message: Message):
    await message.answer(
        text="Тестируем",
        reply_markup=get_date()
    )
