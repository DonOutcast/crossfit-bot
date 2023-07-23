from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from typing import Callable, Awaitable, Dict, Any, Union
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
