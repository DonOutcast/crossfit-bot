import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    User,
    Target
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
        user_name=user_name.strip().encode("utf-8"),
        account_id=account_id,
        name=name.strip().encode("utf-8"),
        type=type_of_user.strip().encode("utf-8"),
        image=image,
        height=height,
        weight=weight
    )
    session.add(command)
    await session.commit()

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
