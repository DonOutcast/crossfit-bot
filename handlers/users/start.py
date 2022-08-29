from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.default.system_kb import get_menu_keyboard


@dp.message_handler(Command('start'), state="*")
async def enter_test(mes: types.Message):
    await mes.answer('Вы нажали старт', reply_markup=get_menu_keyboard())
