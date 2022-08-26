from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import time

change_the_time = CallbackData('new_time', 'time')
res_time = CallbackData('res_time', 'time')
nums = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

async def inline_set_timer(input_time: int = 0) -> InlineKeyboardMarkup:
    input_time = int(input_time)
    if input_time < 0:
        input_time = 0
    new_time = time.localtime(input_time)

    second_m = 5
    second_b = 15
    minut_m = 60
    minut_b = 60 * 5

    stolb = []

    line = [InlineKeyboardButton(text='⏫', callback_data=change_the_time.new(time=str(input_time + minut_b))),
            InlineKeyboardButton(text='⏫', callback_data=change_the_time.new(time=str(input_time + second_b)))]
    stolb.append(line)

    line = [InlineKeyboardButton(text='🔼', callback_data=change_the_time.new(time=str(input_time + minut_m))),
            InlineKeyboardButton(text='🔼', callback_data=change_the_time.new(time=str(input_time + second_m)))]
    stolb.append(line)

    text = f'{new_time.tm_min}:{new_time.tm_sec:0>2}'
    new_text = ''
    for char in text:
        if char.isdigit():
            new_text += nums[int(char)]
        else:
            new_text += char


    line = [InlineKeyboardButton(text=new_text, callback_data='-'),]
    stolb.append(line)

    line = [InlineKeyboardButton(text='🔽', callback_data=change_the_time.new(time=str(input_time - minut_m))),
            InlineKeyboardButton(text='🔽', callback_data=change_the_time.new(time=str(input_time - second_m)))]
    stolb.append(line)

    line = [InlineKeyboardButton(text='⏬', callback_data=change_the_time.new(time=str(input_time - minut_b))),
            InlineKeyboardButton(text='⏬', callback_data=change_the_time.new(time=str(input_time - second_b)))]
    stolb.append(line)

    line = [InlineKeyboardButton(text='Принять', callback_data=res_time.new(time=str(input_time))), ]
    stolb.append(line)

    keyboard = InlineKeyboardMarkup(inline_keyboard=stolb)
    return keyboard
