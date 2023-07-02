from enum import Enum
from typing import Optional
from aiogram.filters.callback_data import CallbackData


class TimeAction(str, Enum):
    ignore = "IGNORE"
    time = "TIME"
    now = "NOW"


class AioTimeCallbackData(CallbackData, prefix="simple_calendar"):
    action: TimeAction
    time: Optional[str]
