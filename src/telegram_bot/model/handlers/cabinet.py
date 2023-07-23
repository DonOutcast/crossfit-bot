from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from model.template.templates import render

from model.fsm import TaskStates

from images import (
    TYPE_MARKUP,
    GOOD_BY,
)

from model.keyboards import (
    back_to_menu,
    task_keyboard,
    task_choice_keyboard,
)

from model.call_back_data import (
    TaskNoCallBackData,
    TaskYesCallBackData,
    DateCallbackData,
)

from model.utils import (
    check_length_value,
)

cabinet_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@cabinet_router.message(F.text == "Цели 🎯", flags=headers)
async def cmd_tasks(message: Message):
    await message.answer(
        text=render.render_template("cabinet/task.html"),
        reply_markup=task_keyboard
    )


@cabinet_router.message(F.text == "Поставить цель 📈")
async def cmd_task_start(message: Message):
    await message.answer(
        text=render.render_template("cabinet/begin.html"),
        reply_markup=task_choice_keyboard
    )


@cabinet_router.callback_query(TaskNoCallBackData.filter(), flags=headers)
async def cmd_no(query: CallbackQuery) -> None:
    await query.message.delete()
    await query.message.answer_sticker(
        sticker=GOOD_BY
    )
    await query.message.answer(
        text=render.render_template(template_name="login/no.html",
                                    data={"user_name": query.message.chat.username})
    )


@cabinet_router.callback_query(TaskYesCallBackData.filter(), flags=headers)
async def cmd_yes(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.delete()
    await query.message.answer_sticker(
        sticker=TYPE_MARKUP
    )
    await query.message.answer(
        text=render.render_template(template_name="cabinet/name.html"),
        reply_markup=back_to_menu
    )
    await state.set_state(TaskStates.name)


@cabinet_router.message(F.content_type.in_("text"), TaskStates.name, flags=headers)
async def cmd_task_name(message: Message, state: FSMContext) -> None:
    if check_length_value(max_size=80, user_size=message.text):
        await state.update_data(name=message.text)
        await message.answer(
            text=render.render_template(template_name="cabinet/date_start.html")
        )
        await message.answer(
            text="Crossfit\n    Kzn",
            # reply_markup=get_date()
        )
        await state.set_state(TaskStates.begin)
    else:
        await state.clear()
        await message.answer(
            text=render.render_template(template_name="error/value.html", data={"operation": "Название цели"})
        )
        await state.set_state(TaskStates.name)


@cabinet_router.message(F.content_type.in_("callback_data"), TaskStates.begin)
async def cmd_task_begin_date(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Crossfit\n    Kzn",
        # reply_markup=get_date()
    )


@cabinet_router.callback_query(DateCallbackData.filter(F.type == "refresh"))
async def refresh_date(query: CallbackQuery, callback_data: CallbackData) -> None:
    await query.message.edit_reply_markup(
        inline_message_id=query.inline_message_id,
        # reply_markup=get_date(datetime.strptime(callback_data.dict().get("date"), "%Y/%m")),
    )


# @cabinet_router.callback_query(DateCallbackData.filter(F.type == "get_date"))
# async def
