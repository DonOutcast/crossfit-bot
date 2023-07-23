from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from model.fsm.login import LoginStates
from model.utils import check_float_value
from model.template.templates import render
from model.keyboards import get_type_keyboards

from model.database.request.requests import (
    add_user,
    if_user_exists,
)

from model.keyboards import (
    back_to_menu,
    personal_cabinet_keyboard,
    login_choice_keyboard,
)

from model.call_back_data import (
    TypeBeginnerCallBackData,
    TypeProceedingCallBackData,
    TypeProfessionalBackData
)

from model.call_back_data import (
    LoginYesCallBackData,
    LoginNoCallBackData
)

from images import (
    LOGIN,
    GOOD_BY,
    TYPE_MARKUP,
    PHOTO,
    WELCOME_TO_CABINET,
)

login_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}


@login_router.message(F.text == "Личный кабинет 🔐", flags=headers)
async def cmd_login(message: Message, session: AsyncSession):
    if data := await if_user_exists(session, message.from_user.id):
        await message.answer(
            text=render.render_template(template_name="cabinet/start.html"),
            reply_markup=personal_cabinet_keyboard
        )
        await message.answer_sticker(
            sticker=WELCOME_TO_CABINET,
        )
    else:
        await message.answer(
            text=render.render_template(template_name="login/login.html")
        )
        await message.answer_sticker(
            sticker=LOGIN,
            reply_markup=login_choice_keyboard
        )


@login_router.callback_query(LoginNoCallBackData.filter(), flags=headers)
async def cmd_login_no(query: CallbackQuery) -> None:
    await query.message.delete()
    await query.message.answer_sticker(
        sticker=GOOD_BY
    )
    await query.message.answer(
        text=render.render_template(template_name="login/no.html",
                                    data={"user_name": query.message.chat.username})
    )


@login_router.callback_query(LoginYesCallBackData.filter(), flags=headers)
async def cmd_login_yes(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.delete()
    await query.message.answer_sticker(
        sticker=TYPE_MARKUP
    )
    await query.message.answer(
        text=render.render_template(template_name="login/name.html"),
        reply_markup=back_to_menu
    )
    await state.set_state(LoginStates.name)


@login_router.message(F.content_type.in_("text"), LoginStates.name, flags=headers)
async def cmd_login_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer_sticker(
        sticker=TYPE_MARKUP
    )
    await message.answer(
        text=render.render_template(template_name="login/type.html"),
        reply_markup=get_type_keyboards()
    )
    await state.set_state(LoginStates.type)


@login_router.callback_query(
    TypeBeginnerCallBackData.filter(),
    flags=headers)
async def cmd_login_beginner(query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(type="Новичок")
    await state.set_state(LoginStates.image)
    await query.message.answer_sticker(
        sticker=PHOTO
    )
    await query.message.answer(
        text=render.render_template(template_name="login/image.html"),
        reply_markup=back_to_menu
    )


@login_router.callback_query(TypeProceedingCallBackData.filter(), flags=headers)
async def cmd_login_beginner(query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(type="Продолжаю")
    await state.set_state(LoginStates.image)
    await query.message.answer_sticker(
        sticker=PHOTO
    )
    await query.message.answer(
        text=render.render_template(template_name="login/image.html"),
        reply_markup=back_to_menu
    )


@login_router.callback_query(TypeProfessionalBackData.filter(), flags=headers)
async def cmd_login_beginner(query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(type="Профи")
    await state.set_state(LoginStates.image)
    await query.message.answer_sticker(
        sticker=PHOTO
    )
    await query.message.answer(
        text=render.render_template(template_name="login/image.html"),
        reply_markup=back_to_menu
    )


@login_router.message(
    F.content_type.in_("photo"),
    LoginStates.image,
    flags=headers
)
async def cmd_login_image(message: Message, state: FSMContext) -> None:
    await state.update_data(image=message.photo[0].file_id)
    await state.set_state(LoginStates.height)
    await message.answer_sticker(
        sticker=TYPE_MARKUP
    )
    await message.answer(
        text=render.render_template(template_name="login/height.html"),
        reply_markup=back_to_menu
    )


@login_router.message(LoginStates.height, flags=headers)
async def cmd_login_height(message: Message, state: FSMContext) -> None:
    if check_float_value(message.text):
        await state.update_data(height=message.text)
        await state.set_state(LoginStates.weight)
        await message.answer_sticker(
            sticker=TYPE_MARKUP
        )
        await message.answer(
            text=render.render_template(template_name="login/weight.html"),
            reply_markup=back_to_menu
        )
    else:
        await message.delete()
        await message.answer(
            text=render.render_template(template_name="error/value.html", data={"operation": "рост"}),
            reply_markup=back_to_menu
        )
        await state.set_state(LoginStates.height)


@login_router.message(LoginStates.weight, flags=headers)
async def cmd_login_weight(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if check_float_value(message.text):
        await state.update_data(weight=message.text)
        data = await state.get_data()
        await state.clear()
        await add_user(
            session=session,
            user_name=message.from_user.username,
            account_id=message.from_user.id,
            name=data.get("name"),
            type_of_user=data.get("type"),
            image=data.get("image"),
            height=data.get("height"),
            weight=data.get("weight")
        )
        await message.answer(
            text=render.render_template(template_name="login/success.html"),
            reply_markup=personal_cabinet_keyboard
        )
    else:
        await message.delete()
        await message.answer(
            text=render.render_template(template_name="error/value.html", data={"operation": "вес"}),
            reply_markup=back_to_menu
        )
        await state.set_state(LoginStates.weight)
