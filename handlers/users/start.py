from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp


@dp.message_handler(Command('start'))
async def enter_test(mes: types.Message):
    await mes.answer('Вы нажали старт')
    await mes.answer('Нажмите на /test для теста функции')

