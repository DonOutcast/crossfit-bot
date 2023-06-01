from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession

from model.fsm.login import LoginStates
from model.utils import check_float_value
from model.template.templates import render
from model.keyboards.core_buttons import generate_keyboard, get_login_inline_markup
from model.keyboards import get_type_keyboards
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
    LOGIN,
    GOOD_BY,
    TYPE_MARKUP,
    PHOTO
)

from model.keyboards import (
    back_to_menu,
    personal_cabinet_keyboard
)

cabinet_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@cabinet_router.message(F.text == "Цели 🎯", flags=headers)
async def cmd_tasks(message: Message):
    await message.answer(
        text=render.render_template("cabinet/task.html")
    )
