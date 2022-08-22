from aiogram import Dispatcher, Bot, types

bot = Bot(token="5313740279:AAHcF4QU4xbuKJs3f_zcIBPleWTrXn74M08", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler()
async def cmd_start(message: types.Message):
    await user