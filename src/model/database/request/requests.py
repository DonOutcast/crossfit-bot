import logging
from typing import Optional

from sqlalchemy import select, delete, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from model.database.models import *


async def add_user(
        session: AsyncSession,
        user_name: str,
        account_id: int,
        name: str,
        type_of_user: str,
        image: int,
        height: float,
        weight: float
) -> None:
    command = User(
        user_name=user_name.strip(),
        account_id=account_id,
        name=name.strip(),
        type=type_of_user.strip(),
        image=image,
        height=float(height),
        weight=float(weight)
    )
    session.add(command)
    await session.commit()


async def get_users_list(session: AsyncSession, ):
    result = await session.execute(select(User))

    # Get all the rows as objects
    users = result.scalars().all()
    return [(i.id, i.user_name, i.account_id, i.name, i.type, i.image, i.height, i.weight) for i in users]


async def if_user_exists(session: AsyncSession, account_id: int) -> bool:
    query = select(User).where(User.account_id == account_id)
    response = await session.execute(query)
    return response.scalar()


async def get_calendar_date_by_user(session: AsyncSession, user_id):
    query = select(Calendar.choice_time).where(Calendar.user_id == user_id)
    response = await session.execute(query)
    response = response.scalars()
    return response.all()


async def add_user_event_time(session: AsyncSession, user_id, time):
    query = Calendar(
        user_id=user_id,
        choice_time=time
    )
    session.add(query)
    await session.commit()
    return time.strftime("%H").split()[0]


async def add_selected_date(session: AsyncSession, selected_date, user_account: int):
    try:
        user_id = await get_user_id_by_account_id(session, user_account)
        calendar_date_query = CalendarDate(
            choice_date=selected_date
        )
        session.add(calendar_date_query)
        await session.commit()
        user_calendar_date_query = UserCalendarDate(user_id=user_id, date_id=calendar_date_query.date_id)
        session.add(user_calendar_date_query)
        await session.commit()
    except Exception as e:
        logging.exception(f"Не удалось добавить дату для account_id {user_account}", exc_info=e)


async def get_user_id_by_account_id(session: AsyncSession, user_account: int) -> Optional[int]:
    result = None
    try:
        query = select(User.id).filter_by(account_id=user_account)
        user_id = await session.execute(query)
        result = user_id.scalar_one()
    except Exception as e:
        logging.exception(f"Не удалось получить id по account_id {user_account}", exc_info=e)

    return result


async def remove_selected_date(session: AsyncSession, selected_date, user_account: int) -> bool:
    result = False
    try:
        calendar_date_query = delete(CalendarDate).where(
            CalendarDate.choice_date == selected_date
        ).where(
            CalendarDate.users.any(User.account_id == user_account)
        )
        await session.execute(calendar_date_query)
        await session.commit()
        result = True
    except Exception as e:
        logging.exception(f"Не удалось удалить дату для account_id {user_account}", exc_info=e)
        result = False
    return result


# query = CalendarDate(
#     choice_date=selected_date
# )
# session.add(query)
# await session.flush()
# await session.commit()


async def get_all_days(session: AsyncSession):
    query = select(CalendarDate.choice_date)
    response = await session.execute(query)
    return response.scalars().all()

# async def add_user(
#         user_name: str,
#         account_id: int,
#         name: str,
#         type_of_user: str,
#         image: int,
#         height: float,
#         weight: float
# ):
#     new_user = await User.create(
#         user_name=user_name.strip().encode("utf-8"),
#         account_id=account_id,
#         name=name.strip().encode("utf-8"),
#         type=type_of_user.strip().encode("utf-8"),
#         image=image,
#         height=height,
#         weight=weight
#     )
#     await new_user.save()
#     logging.warning(f"Пользователь {user_name} был добавлен в таблицу User")
#
#
# async def user_exists(account_id: int) -> bool:
#     user = await User.exists(account_id=account_id)
#     return user
