from model.call_back_data import (
    TypeBeginnerCallBackData,
    TypeProceedingCallBackData,
    TypeProfessionalBackData
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_type_keyboards() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Начинаю", callback_data=TypeBeginnerCallBackData().pack()),
            InlineKeyboardButton(text="Продолжаю", callback_data=TypeProceedingCallBackData().pack()),
            InlineKeyboardButton(text="Профи", callback_data=TypeProfessionalBackData().pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
