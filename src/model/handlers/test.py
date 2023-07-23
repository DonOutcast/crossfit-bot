from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from model.call_back_data import AioTimeCallbackData
from model.database.request import *

from model.keyboards import (
    AioTime,
)
from model.keyboards.calendar import (
    AioCalendar,
    AioCalendarCallbackData,
)
from datetime import datetime

test_router = Router()

headers = {"throttling_key": "default", "long_operation": "typing"}

config = {
    'label_next_month': "➡️",
    'label_preview_month': "⬅️",
    'label_next_year': "➡️",
    'label_preview_year': "⬅️",
    # "emoji_after_day": "🗓",
}

AioCalendar.configure(config)


@test_router.message(F.text == "Тест", flags=headers)
async def cmd_tasks(message: Message, session: AsyncSession):
    result = await get_all_days(session=session)
    cal = AioCalendar()
    # cal.all_days = True
    await message.answer(
        text="🗓 Выберите интересующую вас дату:",
        # reply_markup=get_date(),
        reply_markup=cal.get_calendar(selected_days=result)
    )


@test_router.callback_query(
    AioCalendarCallbackData.filter(
        F.action.in_(
            {
                "IGNORE",
                "NEXT_MONTH",
                "PREVIEW_MONTH",
                "NEXT_YEAR",
                "PREVIEW_YEAR",
                "IGNORE",
            }
        )
    )
)
async def catch_calendar(query: CallbackQuery, callback_data: CallbackData, session: AsyncSession) -> None:
    # AioCalendar.all_days = True
    result = await get_all_days(session=session)
    await AioCalendar(
        callback_data.dict().get("year"),
        callback_data.dict().get("month")
    ).process_selection(query, callback_data, selected_days=result)


@test_router.callback_query(
    AioCalendarCallbackData.filter(
        F.action.in_(
            {
                "DAY",
                "TODAY",
            }
        )
    )
)
async def get_test_simple_time(query: CallbackQuery, callback_data: CallbackData, session: AsyncSession) -> None:
    # result = await get_all_days(session=session)

    selected_date = await AioCalendar(
        callback_data.dict().get("year"),
        callback_data.dict().get("month")
    ).process_selection(query, callback_data)

    await add_selected_date(session, selected_date=selected_date[-1], user_account=query.from_user.id)
    await query.message.delete()
    await query.message.answer(text="Выберите время ", reply_markup=AioTime().get_time())


@test_router.callback_query(
    AioCalendarCallbackData.filter(
        F.action.in_(
            {
              "SELECTED",
            }
        )
    )
)
async def remove_selected_day_from_calendar(
        query: CallbackQuery,
        callback_data: CallbackData,
        session: AsyncSession
) -> None:

    result = await AioCalendar(
        callback_data.dict().get("year"),
        callback_data.dict().get("month")
    ).process_selection(query, callback_data)
    print(f"RESULT I AM in HERE {result}")
    await remove_selected_date(session, selected_date=result[-1], user_account=query.from_user.id)

    await query.message.delete()
    await query.message.answer(text="Выберите время ", reply_markup=AioTime().get_time())


# @test_router.callback_query(DateCallbackData.filter(F.type == "refresh"))
# async def refresh_date(query: CallbackQuery, callback_data: CallbackData) -> None:
#     await query.message.edit_reply_markup(
#         inline_message_id=query.inline_message_id,
#         reply_markup=get_date(datetime.strptime(callback_data.dict().get("date"), "%Y/%m")),
#     )


# @test_router.callback_query(
#     AioTimeCallbackData.filter(
#         F.action.in_(
#             "TIME"
#         )
#     )
# )
# async def get_time(query: CallbackQuery, callback_data: CallbackData, session: AsyncSession) -> None:
#     result = await AioTime().process_selection(query, callback_data)
#     print(result)


@test_router.callback_query(AioTimeCallbackData.filter(F.action.in_("TIME")))
async def refresh_time(query: CallbackQuery, session: AsyncSession, callback_data: AioTimeCallbackData) -> None:
    user_date = await get_calendar_date_by_user(session=session, user_id=query.from_user.id)
    # if not user_date:
    user_selected_time = await add_user_event_time(
        session, query.from_user.id,
        datetime.strptime(callback_data.dict().get("time"), "%H").time()
    )
    callback_data.time += ":00 🔰"
    await AioTime().process_selection(query, callback_data)

# @test_router.callback_query(DateCallbackData.filter(F.type == "get_date"))
# async def save_date_get_time(query: CallbackQuery, callback_data: CallbackData) -> None:
#     # await query.answer(text="Вы выбрали дату", show_alert=True)
#     await query.message.answer(text="Выберите дату")
#     await query.message.edit_reply_markup(
#         inline_message_id=query.inline_message_id,
#         reply_markup=get_time(callback_data.dict().get("date"))
#     )
