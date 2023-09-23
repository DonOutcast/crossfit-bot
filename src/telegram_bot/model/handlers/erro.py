import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ContentType

from model.template.templates import RenderTemplate

render = RenderTemplate()

error_router = Router()


@error_router.message(
    F.content_type.in_(
        {
            'text',
            'emoji',
            'sticker',
            'photo',
            'audio',
            'document',
            'video',
            'video_note',
            'voice',
            'has_media_spoiler',
            'contact',
            'game',
            'poll',
            'venue',
        }
    ),
    flags={"long_operation": "typing"}
)
async def error_message(message: Message):
    try:
        await message.delete()
    except (Exception,):
        # TODO logging
        pass
    await message.answer(text=render.render_template("error/error.html", {"user_name": message.from_user.first_name}))


@error_router.message(
    F.content_type.in_(
        {
            'dice',
        }
    ),
    flags={"long_operation": "typing"}
)
async def error_dice(message: Message):
    try:
        await message.delete()
    except (Exception,):
        # TODO logging
        pass
    await message.answer(text=render.render_template("error/dice.html", {"user_name": message.from_user.first_name}))
