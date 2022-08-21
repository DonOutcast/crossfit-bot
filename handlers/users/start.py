from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from loader import dp


@dp.message_handler(Command('start'), state="*")
async def enter_test(mes: types.Message, state: FSMContext):
    await state.reset_data()
    await mes.answer('Привет! поздравляю! ты в чат-боте "Говори на миллион"👍', reply_markup=ReplyKeyboardRemove())
    await mes.answer('Напиши свое имя',
                     reply_markup=ReplyKeyboardRemove())
