from typing import List, Tuple

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.cruds import auths as auth_api
from api.models import users as user_model
from api.schemas import users as user_schema


async def create_user(db: AsyncSession, user_create: user_schema.UserCreate) -> user_model.User:
    user = user_model.User(**user_create.dict())
    user.password = await auth_api.get_hashed_password(user.password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_all_users(db: AsyncSession) -> List[user_model.User]:
    result: Result = await db.execute(
        select(user_model.User.id, user_model.User.name, user_model.User.password)
    )
    return result.all()


async def find_by_id(db: AsyncSession, user_id: int) -> user_model.User | None:
    result: Result = await db.execute(select(user_model.User).filter_by(id=user_id))
    user = result.first()
    return user[0] if user else None


async def find_by_name(db: AsyncSession, username: str) -> user_model.User:
    result: Result = await db.execute(select(user_model.User).filter_by(name=username))
    user = result.first()
    return user[0] if user else None


async def update_user(
    db: AsyncSession, current_user: user_model.User, updated_user: user_schema.UserCreate
) -> user_model.User:
    if updated_user.name != "":
        current_user.name = updated_user.name

    if updated_user.password != "":
        current_user.password = await auth_api.get_hashed_password(updated_user.password)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


async def delete_user(db: AsyncSession, user: user_model.User) -> None:
    await db.delete(user)
    await db.commit()
    return
