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
            'sticker',
            'audio',
            'document',
            'video',
            'video_note',
            'voice',
            'has_media_spoiler',
            'contact',
            'dice',
            'game',
            'poll',
            'venue',
            }
        ),
    flags={"long_operation": "typing"}
    )
async def error_message(message: Message):
    await message.delete()
    await message.answer(text=render.render_template("error.html", {"user_name": message.from_user.first_name}))
