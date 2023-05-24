from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile

import random

from model.template.templates import render

cat_router = Router()
headers = {"throttling_key": "default", "long_operation": "typing"}


@cat_router.message(F.text == "Милота 🐱", flags=headers)
async def user_start(message: Message):
    cat_number = str(random.randint(1, 10))
    await message.answer_photo(text=render.render_template(template_name="cat.html"),
                               photo=FSInputFile('../../misc/images/' + cat_number + '.jpg'))
