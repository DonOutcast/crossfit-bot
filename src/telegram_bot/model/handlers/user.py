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
    pprint(message)
    await message.answer(text=render.render_template(template_name="start.html"), reply_markup=menu_keyboard)


@user_router.message(Command(commands="categories"), flags=headers)
async def show_list_categories(message: Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    await message.answer(text=render.render_template("category.html", {"categories": categories}))
