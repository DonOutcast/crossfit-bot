from aiohttp import ClientSession, ClientTimeout
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from typing import Callable, Dict, Any, Awaitable, Union


class AiohttpSessionCallbackMiddleware(BaseMiddleware):

    def __init__(self, aiohttp_timeout: ClientTimeout):
        super().__init__()
        self.aiohttp_session_timeout = aiohttp_timeout

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        async with ClientSession(timeout=self.aiohttp_session_timeout) as aiohttp_session:
            aiohttp_session.connector._ssl = False
            data["aiohttp_session"] = aiohttp_session
            return await handler(event, data)
