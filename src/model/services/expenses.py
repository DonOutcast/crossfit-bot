import re
import pytz
import datetime
from typing import List, NamedTuple, Optional

from model.database.db import test_db

from model.services.categories import Categories

from model.errors.exception import NotCorrectMessage


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    """
    Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот.
    """
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text
    )
    inserted_row_id = test_db.insert_item_to_table(
        "expense",
        {
            "amount": parsed_message.amount,
            "created": _get_now_formatted(),
            "category_codename": category.codename,
            "raw_text": raw_message
        }
    )
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def get_today_statistics() -> str:
    """
    Возвращает строкой статистику расходов за сегодня
    :return:
    """
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   "from expense where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    cursor.execute("select sum(amount) "
                   "from expense where date(created)=date('now', 'localtime') "
                   "and category_codename in (select codename "
                   "from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Расходы сегодня:\n"
            f"всего — {all_today_expenses} руб.\n"
            f"базовые — {base_today_expenses} руб. из {_get_budget_limit()} руб.\n\n"
            f"За текущий месяц: /month")


def _parse_message(raw_message: str) -> Message:
    """
    Парсит текст пишедшего сообщения о новом расходе.
    :param raw_message:
    :return:
    """
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) or not regexp_result.group(1) or not regexp_result.group(2):
        raise NotCorrectMessage("Не могу понять сообщение. Напишите сообщение в формате, "
                                "например:\n1500 метро")
    amount = int(regexp_result.group(1).replace(" ", ""))
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_budget_limit() -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    return test_db.select_from_table("budget", ["daily_limit"])[0]["daily_limit"]