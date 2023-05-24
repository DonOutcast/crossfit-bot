from bs4 import BeautifulSoup
from aiohttp import ClientSession
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from model.services.crud_currency import fetch_xml
from model.services.currency_base import get_all_currency
from model.call_back_data.call_back_data_currency import ChangePage, CourseCurrency


def create_currency_keyboard(
        currency_index: int,
        names_of_currency: list,
        page_size: int = 15,
) -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=keyboard, callback_data=CourseCurrency(name=keyboard).pack()) for keyboard in
               names_of_currency if
               len(keyboard.encode("utf-8")) < 64]
    page_count = (len(buttons) + page_size - 1) // page_size  # количество страниц
    current_page = currency_index // page_size  # текущая страница
    start_index = current_page * page_size  # индекс первой кнопки на текущей странице
    end_index = start_index + page_size  # индекс последней кнопки на текущей странице
    keyboards = [buttons[i:i + 3] for i in range(start_index, end_index, 3)]
    prev_page = current_page - 1 if current_page > 0 else page_count - 1  # номер предыдущей страницы
    next_page = (current_page + 1) % page_count  # номер следующей страницы
    keyboards += [
        [
            InlineKeyboardButton(text="⬅️", callback_data=ChangePage(page=prev_page * page_size).pack()),
            InlineKeyboardButton(text=f"{current_page + 1}/{page_count}", callback_data=" "),
            InlineKeyboardButton(text="➡️", callback_data=ChangePage(page=next_page * page_size).pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboards)


async def get_currency_markup(aiohttp_session: ClientSession, currency_index: int,
                              page_size: int = 15) -> InlineKeyboardMarkup:
    soup: BeautifulSoup = await fetch_xml(aiohttp_session)
    currency_list: list = get_all_currency(soup)
    return create_currency_keyboard(currency_index=currency_index, names_of_currency=currency_list, page_size=page_size)
