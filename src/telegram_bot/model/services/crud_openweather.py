import json
from aiohttp import ClientSession
from configurate.config import settings
from .weather_help import Coordinates


async def fetch_json(aiohttp_session: ClientSession, coordinates: Coordinates) -> json:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates.latitude}&lon={coordinates.longitude}" \
          f"&appid={settings.openweather_token.get_secret_value()}&lang=ru&units=metric"
    try:
        async with aiohttp_session.get(url) as response:
            return await response.json()
    except Exception:
        print("Проблемы")
