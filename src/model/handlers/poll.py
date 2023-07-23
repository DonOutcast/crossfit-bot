from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from model.fsm.poll import PollStates
from model.template.templates import RenderTemplate
from model.keyboards.core_buttons import generate_keyboard

render = RenderTemplate()

poll_router = Router()
poll_menu_buttons = generate_keyboard(
    [
        [
            "Создать опрос"
        ],
        [
            "Вернуться в главное меню 📜"
        ]
    ]
)


@poll_router.message(F.text == "Опрос 📝")
async def cmd_poll(message: Message):
    await message.answer(text=render.render_template("poll.html"), reply_markup=poll_menu_buttons)
    await message.answer(text=str(message.chat.id))


# @poll_router.message(
#     F.content_type.in_(
#         {
#             'sticker',
#             'audio',
#             'document',
#             'video',
#             'video_note',
#             'voice',
#             'has_media_spoiler',
#             'contact',
#             'dice',
#             'game',
#             'poll',
#             'venue',
#         }
#     ),
#     flags={"long_operation": "typing"}
# )
# async def back_poll(message: Message):
#     await message.delete()


@poll_router.message(F.text == "Создать опрос")
async def create_poll_start(message: Message, state: FSMContext):
    await message.answer(text=render.render_template("start_poll.html"))
    await state.set_state(PollStates.question)


@poll_router.message(PollStates.question)
async def question_poll(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(text=render.render_template("question_poll.html"))
    await state.set_state(PollStates.answers)


@poll_router.message(PollStates.answers)
async def answers_poll(message: Message, state: FSMContext):
    await state.update_data(answers=message.text.split())
    await message.answer(text=render.render_template("answers_poll.html"))
    await state.set_state(PollStates.chat_id)


@poll_router.message(PollStates.chat_id)
async def chat_id_poll(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(chat_id=message.text)
    data = await state.get_data()
    try:
        await bot.send_poll(chat_id=data.get("chat_id"), question=data.get("question"), options=data.get("answers"))
    except Exception:
        await message.answer(text=render.render_template("poll_error.html"))
    finally:
        await state.clear()
