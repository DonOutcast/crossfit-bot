import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    User,
    Target,
    Calendar
)


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
