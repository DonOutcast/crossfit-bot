from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from model.template.templates import render


from model.keyboards.core_buttons import generate_keyboard

menu_keyboard = generate_keyboard(
    [
        [
            "Личный кабинет 🔐",
            "Что по погоде 🌤️"
        ],
        [
            "Погода 🌤️",
            "Валюта 💰"
        ],
        [
            "Милота 🐱",
            "Опрос 📝"
        ],

    ],
)
user_router = Router()
headers = {"throttling_key": "default", "long_operation": "typing"}


@user_router.message(CommandStart(), flags=headers)
async def user_start(message: Message):
    from pprint import pprint
    await message.answer(text=render.render_template(template_name="start.html"), reply_markup=menu_keyboard)

