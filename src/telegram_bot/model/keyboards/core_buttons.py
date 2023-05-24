from typing import List
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup



menu_buttons = [
    [KeyboardButton(text="Погода 🌤️"), KeyboardButton(text="Валюта 💰")],
    [KeyboardButton(text="Милота 🐱"), KeyboardButton(text="Опрос 📝")],
    
]

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=menu_buttons, resize_keyboard=True,)


def generate_keyboard(buttons: List[List[str]], resize_keyboard=True, request_location=False) -> ReplyKeyboardMarkup:
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
            else:
                row.append(KeyboardButton(text=button_text))
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=resize_keyboard)

# [
#     KeyboardButton(text='Локация', request_location=True),
# ],
