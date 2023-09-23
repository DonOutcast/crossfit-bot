import json
from typing import Literal
from datetime import datetime

from .weather_help import (
    Celsius,
    Weather,
    WeatherType,
    ApiServicesError
)


def get_weather(response_json: json) -> Weather:
    weather = _parse_openweather_response(response_json)
    return weather


def _parse_openweather_response(open_weather_response: json) -> Weather:
    return Weather(
        temperature=_parse_temperature(open_weather_response),
        weather_type=_parse_weather_type(open_weather_response),
        sunrise=_parse_sun_time(open_weather_response, "sunrise"),
        sunset=_parse_sun_time(open_weather_response, "sunset"),
        city=_parse_city(open_weather_response)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServicesError
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type.value
    raise ApiServicesError


def _parse_sun_time(
        openweather_dict: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict["name"]
