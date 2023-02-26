from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models.likes import Like as LikeModel
from api.models.tweets import Tweet as TweetModel
from api.models.users import User as UserModel
from api.schemas import tweets as tweet_schema


async def get_all_tweets(db: AsyncSession) -> List[TweetModel]:
    return (await db.execute(select(TweetModel))).scalars().all()


async def get_all_tweets_which_user_likes(
    db: AsyncSession, user_id: int
) -> List[TweetModel]:
    """Get all tweets which a user likes"""
    stmt = select(TweetModel).join(LikeModel).where(LikeModel.user_id == user_id)
    return (await db.execute(stmt)).scalars().all()


async def create_tweet(
    db: AsyncSession, current_user: UserModel, tweet_body: tweet_schema.TweetCreate
) -> TweetModel:
    tweet = TweetModel(**tweet_body.dict())
    current_user.tweets.append(tweet)

    db.add(current_user)
    await db.commit()
    await db.refresh(tweet)

    return tweet


async def find_by_id(db: AsyncSession, tweet_id: int) -> TweetModel | None:
    stmt = (
        select(TweetModel)
        .options(selectinload(TweetModel.likes))
        .filter_by(id=tweet_id)
    )
    return (await db.execute(stmt)).scalar()


async def update_tweet(
    db: AsyncSession, updated: TweetModel, tweet_body: tweet_schema.TweetUpdate
) -> TweetModel:
    updated.message = tweet_body.message

    db.add(updated)
    await db.commit()
    await db.refresh(updated)

    return updated


async def delete_tweet(db: AsyncSession, deleted: TweetModel) -> None:
    await db.delete(deleted)
    await db.commit()
    return None
