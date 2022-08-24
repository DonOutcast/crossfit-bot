from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

start_timer = CallbackData('start_timer', 'time')


async def inline_start_timer(input_time):
    line = [InlineKeyboardButton(text='Запустить', callback_data=start_timer.new(time=str(input_time)))]
    keyboard = [line]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
