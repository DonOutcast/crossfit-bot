import tortoise

from models import (
    User,
    Target
)


async def add_user(
        user_name: str,
        account_id: int,
        name: str,
        type_of_user: str,
        image: int,
        height: float,
        weight: float
):
    new_user = await User.create(
        user_name=user_name,
        account_id=account_id,
        name=name,
        type=type_of_user,
        image=image,
        height=height,
        weight=weight
    )
    await new_user.save()
