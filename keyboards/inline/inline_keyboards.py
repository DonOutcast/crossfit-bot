from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_complex():
    keyboards = []
    line = [InlineKeyboardButton(text="Добавить комплекс", callback_data='_add_complex')]
    keyboards.append(line)
    line = [InlineKeyboardButton(text="Выбрать из списка", callback_data='_choice_complex')]
    keyboards.append(line)
    return InlineKeyboardMarkup(inline_keyboard=keyboards)


def get_training():
    keyboards = []
    line = [InlineKeyboardButton(text="Добавить тренеровку", callback_data='_add_training')]
    keyboards.append(line)
    line = [InlineKeyboardButton(text="Выбрать из списка", callback_data='_choice_training')]
    keyboards.append(line)
    return InlineKeyboardMarkup(inline_keyboard=keyboards)
