from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession

from model.utils import check_float_value
from model.fsm import TaskStates
from model.template.templates import render
from model.database.requests import (
    add_user,
    get_users_list, if_user_exists,
)
from model.call_back_data import (
    TypeBeginnerCallBackData,
    TypeProceedingCallBackData,
    TypeProfessionalBackData
)
from model.call_back_data.login import LoginYesCallBackData, LoginNoCallBackData
from images import (
    TYPE_MARKUP,
    WELCOME_TO_CABINET,
)

from model.keyboards import (
    back_to_menu,
    task_keyboard,
)

cabinet_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@cabinet_router.message(F.text == "Цели 🎯", flags=headers)
async def cmd_tasks(message: Message):
    await message.answer(
        text=render.render_template("cabinet/task.html"),
        reply_markup=task_keyboard
    )
    await message.answer_sticker(
        sticker=WELCOME_TO_CABINET
    )




