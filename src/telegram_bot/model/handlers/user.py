from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from model.template.templates import render

from model.keyboards import menu_keyboard


user_router = Router()
headers = {"throttling_key": "default", "long_operation": "typing"}


@user_router.message(CommandStart(), flags=headers)
async def user_start(message: Message):
    await message.answer(
        text=render.render_template(template_name="start.html"),
        reply_markup=menu_keyboard
    )
