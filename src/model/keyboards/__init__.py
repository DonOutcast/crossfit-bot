from .inline_keyboards import get_type_keyboards
from .core_buttons import (
    generate_keyboard,
    generate_inline_keyboard,
    login_choice_keyboard,
    task_choice_keyboard,
)
from .time import AioTime

personal_cabinet_keyboard = generate_keyboard(
    [
        [
            "Статус 📊",
            "Цели 🎯",
        ],
        [
            "Тренеровки",
            "Site",
        ],
        [
            "Вернуться в главное меню 📜",
        ],
    ],
    resize_keyboard=True,
    web_app_url="https://donoutcast.github.io/Donbook.github.io/"
)

back_to_menu = generate_keyboard(
    [
        [
            "Вернуться в главное меню 📜",
        ],
    ],
    resize_keyboard=True,
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
        [
            "Тест",
            "SItE",
        ],

    ],
    resize_keyboard=True,
    web_app_url="https://crossfit-frontend.vercel.app/",
)

task_keyboard = generate_keyboard(
    [
        [
            "Мои цели 🗃",
            "Поставить цель 📈",
        ],
        [
            "Вернуться в главное меню 📜",
        ],
    ],
    resize_keyboard=True
)
