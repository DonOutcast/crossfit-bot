from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, Location
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

from model.filters.admin import AdminFilter
from model.template.templates import RenderTemplate

from model.fsm.coordinates import CoordinatesStates
render = RenderTemplate()

admin_router = Router()
# headers = {"throttling_key": "default", "long_operation": "typing"}
# admin_router.message.filter(AdminFilter())

# menu_buttons = [
#     [
#         KeyboardButton(text='Локация', request_location=True),
#     ],

# ]

# menu_keyboard = ReplyKeyboardMarkup(
#     keyboard=menu_buttons, resize_keyboard=True)

# @admin_router.message(CommandStart(), flags=headers)
# async def admin_start(message: Message):
#     print("im admin command")
#     await message.reply("Доп права!", reply_markup=menu_keyboard)
#     print(message.location)

# @admin_router.message(F.location)
# async def location_admin(message: Message, state: FSMContext):
#     await state.set_state(CoordinatesStates.longitude)

# @admin_router.message(CoordinatesStates.longitude)
# async def longitude_function(message: Message, state: FSMContext):
#     await state.update_data(longitude=message.location.longitude)
#     await state.set_state(CoordinatesStates.latitude)

# @admin_router.message(CoordinatesStates.latitude)
# async def latiude_function(message: Message, state: FSMContext):
#     await state.update_data(latitude=message.location.longitude)
#     data = await state.get_data()
#     print(data.latitude)
#     print(data.longitude)
