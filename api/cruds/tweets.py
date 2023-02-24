from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.cruds import auths as auth_api
from api.models import tweets as tweet_model
from api.models import users as user_model
from api.schemas import tweets as tweet_schema
from api.schemas import users as user_schema


async def get_all_tweets(db: AsyncSession) -> List[tweet_model.Tweet]:
    return (await db.execute(select(tweet_model.Tweet))).fetchall()


async def create_tweet(
    db: AsyncSession, current_user: user_model.User, tweet_body: tweet_schema.TweetCreate
) -> tweet_model.Tweet:
    tweet = tweet_model.Tweet(**tweet_body.dict())
    tweet.user = current_user
    tweet.user_id = current_user.id

    db.add(tweet)
    await db.commit()
    await db.refresh(tweet)

    return tweet
