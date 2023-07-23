from bs4 import BeautifulSoup
from model.services.currency_help import Course


def get_all_currency(soup_result: BeautifulSoup) -> list[list[str]]:
    return [currency.find("name").text for currency in soup_result.find_all("valute")]


def get_course_from_inlines(soup_result: BeautifulSoup, name_of_currency: str):
    for valute in soup_result.find_all("valute"):
        if valute.find("name").text == name_of_currency:
            currency_value = valute.find("value").text.replace(',', '.')
            currency_nominal = valute.find("nominal").text
            value = float(currency_value) / int(currency_nominal)
            return round(value, 2)


def _parse_course_response(soup_response: BeautifulSoup) -> Course:
    return Course(
        exchange_rate=_parse_exchange_rate(soup_response),
        nominal=_parse_nominal(soup_response),
        name=_parse_name(soup_response),
    )


def _parse_exchange_rate(soup_response: BeautifulSoup) -> float:
    return round(float(soup_response.find("value").text.replace(',', '.')), 2)


def _parse_nominal(soup_response: BeautifulSoup) -> float:
    return int(soup_response.find("nominal").text)


def _parse_name(soup_response: BeautifulSoup) -> str:
    return soup_response.find("name").text


def get_course(soup_response: BeautifulSoup) -> Course:
    course = _parse_course_response(soup_response)
    return course


def check_count(count: str) -> bool:
    try:
        count = float(count)
        if count > 0:
            return True
    except Exception:
        return False
