from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models.likes import Like as LikeModel
from api.models.users import User as UserModel


async def get_all_likes(db: AsyncSession, user_id: int) -> List[LikeModel]:
    return (await db.execute(select(LikeModel).filter(LikeModel.user_id == user_id))).fetchall()


async def find_by_user_id_and_tweet_id(db: AsyncSession, user_id: int, tweet_id: int) -> LikeModel:
    fav = await db.execute(
        select(LikeModel).filter(LikeModel.user_id == user_id).filter(LikeModel.tweet_id == tweet_id)
    )
    return fav.first()


async def create_like(db: AsyncSession, tweet_id: int, current_user: UserModel) -> LikeModel:
    like = LikeModel(tweet_id=tweet_id, user_id=current_user.id)

    db.add(like)
    await db.commit()
    await db.refresh(like)

    return like


async def delete_like(db: AsyncSession, like_model: LikeModel) -> None:
    db.delete(like_model)
    await db.commit()
    return
