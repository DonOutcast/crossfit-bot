import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp, bot
from keyboards import inline_set_timer, change_the_time, res_time, inline_start_timer, start_timer


@dp.message_handler(Command('test'))
async def get_timer(mes: types.Message):
    await mes.answer('Вы зашли в тест функции\n'
                     'Дання функция находится в разработке\n'
                     'Это часть большого проекта, так что не стоит рассматривать данную функцию как отдельную программу')
    await mes.answer('Вам представлен инструмент для настройки и запуска таймера\n'
                     'Нажимая на стрелочки настройте время для таймера\n'
                     'Потом нажмите на кнопку "Принять"\n'
                     'Минуты - Секунды'
                     , reply_markup=await inline_set_timer())


@dp.callback_query_handler(change_the_time.filter())
async def enter_test(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=call.message.text,
        reply_markup=await inline_set_timer(callback_data['time']))


@dp.callback_query_handler(res_time.filter())
async def enter_test(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    time = callback_data["time"]
    await call.message.answer(f'Таймер на {time} секунд', reply_markup=await inline_start_timer(time))


@dp.callback_query_handler(start_timer.filter())
async def enter_test(call: types.CallbackQuery, callback_data: dict):
    # await call.message.delete()
    time = int(callback_data["time"])
    start_time = 3
    for first in range(start_time):
        await asyncio.sleep(1)
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'Через {start_time-first} запустится таймер на {time} секунд',
            reply_markup=None)

    for last in range(time):
        await asyncio.sleep(1)
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'Осталось {time-last} сек',
            reply_markup=None)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'Время вышло',
        reply_markup=None)


@dp.callback_query_handler()
async def enter_test(call: types.CallbackQuery):
    await call.message.answer('не Поймал')
