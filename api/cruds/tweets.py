from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models import tweets as tweet_model
from api.models import users as user_model
from api.schemas import tweets as tweet_schema


async def get_all_tweets(db: AsyncSession) -> List[tweet_model.Tweet]:
    return (await db.execute(select(tweet_model.Tweet))).fetchall()


async def create_tweet(
    db: AsyncSession, current_user: user_model.User, tweet_body: tweet_schema.TweetCreate
) -> tweet_model.Tweet:
    tweet = tweet_model.Tweet(**tweet_body.dict())
    # if either one of them is written, this transaction will work properly.
    tweet.user = current_user
    tweet.user_id = current_user.id

    db.add(tweet)
    await db.commit()
    await db.refresh(tweet)

    return tweet


async def find_by_id(db: AsyncSession, tweet_id: int) -> tweet_model.Tweet | None:
    tweet = (await db.execute(select(tweet_model.Tweet).filter_by(id=tweet_id))).first()
    if not tweet:
        return None
    return tweet[0]


async def update_tweet(
    db: AsyncSession, updated: tweet_model.Tweet, tweet_body: tweet_schema.TweetUpdate
) -> tweet_model.Tweet:
    updated.message = tweet_body.message

    db.add(updated)
    await db.commit()
    await db.refresh(updated)

    return updated


async def delete_tweet(db: AsyncSession, deleted: tweet_model.Tweet) -> None:
    await db.delete(deleted)
    await db.commit()
    return None
