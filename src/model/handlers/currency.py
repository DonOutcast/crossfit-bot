from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from model.template.templates import RenderTemplate
from model.keyboards.core_buttons import generate_keyboard
from model.services.crud_currency import fetch_xml, fetch_one_currency
from model.services.currency_base import get_course, check_count, get_course_from_inlines
from model.keyboards.currency_buttons import get_currency_markup
from model.call_back_data.call_back_data_currency import ChangePage, CourseCurrency
from model.services.currency_help import Course
from model.fsm.currency import CurrencyStates

render = RenderTemplate()

currency_router = Router()
weather_menu_buttons = generate_keyboard(
    [
        [
            "Курс 💵",
            "Курс 💶",

        ],
        [
            "Конвертировать 🧾",
            "Вернуться в главное меню 📜"
        ]

    ],
    request_location=True
)

headers = {"throttling_key": "default", "long_operation": "typing"}


@currency_router.message(F.text == "Валюта 💰", flags=headers)
async def currency_menu(message: Message):
    await message.answer(
        text=render.render_template("currency.html", {"user_name": message.from_user.first_name}),
        reply_markup=weather_menu_buttons)


@currency_router.message(F.text == "Курс 💵", flags=headers)
async def get_today_dollar(message: Message, aiohttp_session: ClientSession):
    soup: BeautifulSoup = await fetch_one_currency(aiohttp_session, "R01235")
    currency: Course = get_course(soup)
    await message.answer(text=render.render_template("format_currency.html", {"currency": currency}))


@currency_router.message(F.text == "Курс 💶", flags=headers)
async def get_today_euro(message: Message, aiohttp_session: ClientSession):
    soup: BeautifulSoup = await fetch_one_currency(aiohttp_session, "R01239")
    currency: Course = get_course(soup)
    await message.answer(text=render.render_template("format_currency.html", {"currency": currency}))


@currency_router.message(F.text == "Конвертировать 🧾", flags=headers)
async def cmd_convector_currency(message: Message, aiohttp_session: ClientSession):
    markup = await get_currency_markup(aiohttp_session, 0)
    await message.answer(text=render.render_template("convector_currency.html"),
                         reply_markup=markup)


@currency_router.callback_query(ChangePage.filter(), flags=headers)
async def all_currency(query: CallbackQuery, callback_data: ChangePage, aiohttp_session: ClientSession):
    markup = await get_currency_markup(aiohttp_session, callback_data.page)
    await query.message.delete()
    await query.message.answer(text=render.render_template("convector_currency.html"),
                               reply_markup=markup)


@currency_router.callback_query(CourseCurrency.filter(), flags=headers)
async def start_convector(query: CallbackQuery, callback_data: CourseCurrency, state: FSMContext,
                          aiohttp_session: ClientSession):
    await state.set_state(CurrencyStates.currency)
    res = await fetch_xml(aiohttp_session)
    await state.update_data(currency=get_course_from_inlines(res, callback_data.name))
    await state.set_state(CurrencyStates.count)
    await query.message.answer(text=render.render_template("count_money.html"))


@currency_router.message(CurrencyStates.count, flags=headers)
async def end_convector(message: Message, state: FSMContext, aiohttp_session: ClientSession):
    if check_count(message.text):
        await state.update_data(count=float(message.text))
        data = await state.get_data()
        await message.answer(text=f"{round(data.get('count') / data.get('currency'), 2)}")
        await state.clear()
    else:
        await message.delete()
        await state.clear()
        markup = await get_currency_markup(aiohttp_session, 0)
        await message.answer(text=render.render_template("convector_currency.html"),
                             reply_markup=markup)
