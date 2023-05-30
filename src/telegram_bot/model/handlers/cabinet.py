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
from model.images.images_ids import (
    LOGIN,
    GOOD_BY,
    TYPE_MARKUP,
    PHOTO
)

personal_cabinet_buttons = generate_keyboard(
    [
        [
            "Статус 📊",
            "Цели 🎯",
        ],
        [
            "Тренеровки",
        ],
        [
            "Вернуться в главное меню 📜"
        ]
    ]
)

back_to_menu = generate_keyboard(
    [
        [
            "Вернуться в главное меню 📜"
        ]
    ]
)

login_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}