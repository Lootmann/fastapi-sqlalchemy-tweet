from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.cruds import auths as auth_api
from api.models.likes import Like as LikeModel
from api.models.tweets import Tweet as TweetModel
from api.models.users import User as UserModel
from api.schemas import users as user_schema


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> UserModel:
    user = UserModel(**user_create.dict())
    user.password = await auth_api.get_hashed_password(user.password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_all_users(db: AsyncSession) -> List[UserModel]:
    results = await db.execute(
        select(UserModel)
        .options(selectinload(UserModel.tweets))
        .options(selectinload(UserModel.likes))
    )
    return results.scalars().all()


async def get_all_users_which_likes_tweet(
    db: AsyncSession, tweet_id: int
) -> List[UserModel]:
    stmt = (
        select(UserModel)
        .join(UserModel.likes)
        .join(LikeModel.tweet)
        .filter(TweetModel.id == tweet_id)
        .options(selectinload(UserModel.tweets), selectinload(UserModel.likes))
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def find_by_id(db: AsyncSession, user_id: int) -> UserModel | None:
    result: Result = await db.execute(
        select(UserModel).filter_by(id=user_id).options(selectinload(UserModel.tweets))
    )
    return result.scalar()


async def find_by_name(db: AsyncSession, username: str) -> UserModel | None:
    # TODO: I think this is pretty heavy preformance. Depends(get_current_user) use this anywhere D:
    result: Result = await db.execute(
        select(UserModel)
        .filter_by(name=username)
        .options(selectinload(UserModel.tweets))
        .options(selectinload(UserModel.likes))
    )
    return result.scalar()


async def update_user(
    db: AsyncSession, updated: UserModel, user_body: user_schema.UserUpdate
) -> UserModel:
    if user_body.name != "":
        updated.name = user_body.name

    if user_body.password != "":
        updated.password = await auth_api.get_hashed_password(user_body.password)

    db.add(updated)
    await db.commit()
    await db.refresh(updated)

    return updated


async def delete_user(db: AsyncSession, deleted: UserModel) -> None:
    await db.delete(deleted)
    await db.commit()
    return None
