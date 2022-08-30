from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from keyboards.default.system_kb import get_menu_keyboard


@dp.message_handler(Text("Вернуться в главное меню 📜"), state="*")
async def cmd_cancel_registration(message: types.Message, state: FSMContext):
    await message.delete()
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Вы вернулись в главное меню', reply_markup=get_menu_keyboard())
        return
    await state.finish()
    await message.answer('Вы вернулись в главное меню', reply_markup=get_menu_keyboard())

@dp.message_handler(Command('start'), state="*")
async def enter_test(mes: types.Message):
    await mes.answer('Вы нажали старт', reply_markup=get_menu_keyboard())
