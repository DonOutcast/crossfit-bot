from typing import List

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup, WebAppInfo
)
from aiogram.filters.callback_data import CallbackData

from model.call_back_data.login import LoginNoCallBackData, LoginYesCallBackData
from model.call_back_data import TaskYesCallBackData, TaskNoCallBackData

menu_buttons = [
    [KeyboardButton(text="Погода 🌤️"), KeyboardButton(text="Валюта 💰")],
    [KeyboardButton(text="Милота 🐱"), KeyboardButton(text="Опрос 📝")],

]

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=menu_buttons, resize_keyboard=True, )


def generate_keyboard(buttons: List[List[str]], resize_keyboard=True, request_location=False,
                      web_app_url=None) -> ReplyKeyboardMarkup:
    """
    Генерирует объект ReplyKeyboardMarkup с заданными кнопками.

    :param buttons: список списков строк, представляющих текст кнопок
    :param resize_keyboard: параметр, определяющий, следует ли изменять размер клавиатуры в соответствии с количеством кнопок (по умолчанию True)
    :param request_location: параметр, определяющий, следует ли добавлять кнопку для запроса местоположения (по умолчанию False)
    :return: объект ReplyKeyboardMarkup
    :raises ValueError: если переданный параметр buttons пуст или содержит пустые списки
    """
    if not buttons or any(not row for row in buttons):
        raise ValueError("buttons parameter cannot be empty or contain empty lists")

    keyboard = []
    for button_row in buttons:
        row = []
        for button_text in button_row:
            if request_location and 'location' in button_text.lower():
                row.append(KeyboardButton(text=button_text.split()[0], request_location=True))
            elif web_app_url and 'site' in button_text.lower():
                row.append(KeyboardButton(text=button_text, web_app=WebAppInfo(url=web_app_url)))
            else:
                row.append(KeyboardButton(text=button_text))
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=resize_keyboard)


# def generate_inline_keyboard(buttons: List[List[tuple[str, str]]]) -> InlineKeyboardMarkup:
#     """
#     Генерирует объект InlineKeyboardMarkup с заданными кнопками.
#
#     :param buttons: список списков пар (текст кнопки, callback_data)
#     :return: объект InlineKeyboardMarkup
#     :raises ValueError: если переданный параметр buttons пуст или содержит пустые списки
#     """
#     if not buttons or any(not row for row in buttons):
#         raise ValueError("buttons parameter cannot be empty or contain empty lists")
#
#     keyboard = []
#     for button_row in buttons:
#         row = []
#         for button_text, callback_data in button_row:
#             row.append(InlineKeyboardButton(text=button_text, callback_data=callback_data))
#         keyboard.append(row)
#     return InlineKeyboardMarkup(inline_keyboard=keyboard)


def generate_inline_keyboard(buttons: List[List[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=buttons)


login_choice_keyboard = generate_inline_keyboard(
    [
        [
            InlineKeyboardButton(text="Да", callback_data=LoginYesCallBackData(answer=True).pack()),
            InlineKeyboardButton(text="Нет", callback_data=LoginNoCallBackData(answer=False).pack())
        ]
    ]
)
task_choice_keyboard = generate_inline_keyboard(
    [
        [
            InlineKeyboardButton(text="Да", callback_data=TaskYesCallBackData(answer=True).pack()),
            InlineKeyboardButton(text="Нет", callback_data=TaskNoCallBackData(answer=False).pack())
        ]
    ]
)
