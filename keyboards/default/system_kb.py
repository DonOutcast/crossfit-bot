from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_menu_keyboard():
    add_button = KeyboardButton("Добавить тренировку 🏹")
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboards.add(add_button)
    return keyboards


def back_menu_keyboard():
    add_button = KeyboardButton("Вернуться в главное меню 📜")
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboards.add(add_button)
    return keyboards
