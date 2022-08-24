from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp, bot
from keyboards import set_timer, change_the_time, res_time


@dp.message_handler(Command('test'))
async def enter_test(mes: types.Message):
    await mes.answer('Вы нажали старт', reply_markup=await set_timer())


@dp.callback_query_handler(change_the_time.filter())
async def enter_test(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=call.message.text,
        reply_markup=await set_timer(callback_data['time']))


@dp.callback_query_handler(res_time.filter())
async def enter_test(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.message.answer(f'Таймер на {callback_data["time"]} секунд')


@dp.callback_query_handler()
async def enter_test(call: types.CallbackQuery):
    await call.message.answer('не Поймал')
