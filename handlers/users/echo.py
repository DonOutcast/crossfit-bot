from aiogram import types
from loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    print(message.text)
    await message.answer(message.text)
