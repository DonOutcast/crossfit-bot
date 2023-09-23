from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from model.template.templates import render

from model.fsm.registration import RegistrationStates

from model.keyboards.core_buttons import generate_keyboard

personal_cabinet_buttons = generate_keyboard(
    [
        [
            "Статус 📊",
            "Мои цели 🎯"
        ],
        [
            "Вернуться в главное меню 📜"
        ]
    ]
)

personal_cabinet_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@personal_cabinet_router.message(CommandStart(), flags=headers)
async def user_start(message: Message):
    await message.answer(text=render.render_template(template_name="start.html"), reply_markup=menu_keyboard)


@personal_cabinet_router.message(Command(commands="categories"), flags=headers)
async def show_list_categories(message: Message):
    """Отправляет список категорий расходов"""
    pass
