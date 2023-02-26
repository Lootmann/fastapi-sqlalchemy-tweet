from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models.likes import Like as LikeModel
from api.models.tweets import Tweet as TweetModel
from api.models.users import User as UserModel


async def get_all_likes(db: AsyncSession, user_id: int) -> List[LikeModel]:
    stmt = await db.execute(select(LikeModel).filter(LikeModel.user_id == user_id))
    return stmt.scalars().all()


async def find_by_user_id_and_tweet_id(
    db: AsyncSession, user_id: int, tweet_id: int
) -> LikeModel | None:
    res = await db.execute(
        select(LikeModel)
        .filter(LikeModel.user_id == user_id)
        .filter(LikeModel.tweet_id == tweet_id)
    )
    like = res.scalar()
    return like if like else None


async def create_like(
    db: AsyncSession, tweet: TweetModel, current_user: UserModel
) -> LikeModel:
    like = LikeModel(tweet_id=tweet.id, user_id=current_user.id)

    tweet.likes.append(like)
    current_user.likes.append(like)

    db.add(tweet)
    db.add(current_user)
    await db.commit()
    await db.refresh(like)

    return like


async def delete_like(db: AsyncSession, like_model: LikeModel) -> None:
    await db.delete(like_model)
    await db.commit()
    return
