from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.cruds import auths as auth_api
from api.models import tweets as tweet_model
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
    results = await db.execute(
        select(user_model.User).options(selectinload(user_model.User.tweets))
    )
    return results.all()


async def find_by_id(db: AsyncSession, user_id: int) -> user_model.User | None:
    result: Result = await db.execute(
        select(user_model.User).filter_by(id=user_id).options(selectinload(user_model.User.tweets))
    )
    user = result.first()
    return user[0] if user else None


async def find_by_name(db: AsyncSession, username: str) -> user_model.User:
    result: Result = await db.execute(select(user_model.User).filter_by(name=username))
    user = result.first()
    return user[0] if user else None


async def update_user(
    db: AsyncSession, updated: user_model.User, user_body: user_schema.UserUpdate
) -> user_model.User:
    if user_body.name != "":
        updated.name = user_body.name

    if user_body.password != "":
        updated.password = await auth_api.get_hashed_password(user_body.password)

    db.add(updated)
    await db.commit()
    await db.refresh(updated)

    return updated
