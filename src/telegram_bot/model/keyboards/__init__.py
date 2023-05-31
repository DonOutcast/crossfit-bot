from aiogram.types import WebAppInfo

from .inline_keyboards import get_type_keyboards
from .core_buttons import generate_keyboard


personal_cabinet_keyboard = generate_keyboard(
    [
        [
            "Статус 📊",
            "Цели 🎯",
        ],
        [
            "Тренеровки",
            "Site"
        ],
        [
            "Вернуться в главное меню 📜"
        ]
    ],
    resize_keyboard=True,
    web_app_url="https://donoutcast.github.io/Donbook.github.io/"
)

back_to_menu = generate_keyboard(
    [
        [
            "Вернуться в главное меню 📜"
        ]
    ]
)

menu_keyboard = generate_keyboard(
    [
        [
            "Личный кабинет 🔐",
            "Что по погоде 🌤️"
        ],
        [
            "Погода 🌤️",
            "Валюта 💰"
        ],
        [
            "Милота 🐱",
            "Опрос 📝"
        ],

    ],
)

