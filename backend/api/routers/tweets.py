from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import auths as auth_api
from api.cruds import tweets as tweet_api
from api.db import get_db
from api.models import tweets as tweet_model
from api.schemas import tweets as tweet_schema

router = APIRouter(tags=["tweets"])


@router.get(
    "/tweets", response_model=List[tweet_schema.Tweet], status_code=status.HTTP_200_OK
)
async def get_all_tweets(
    db: AsyncSession = Depends(get_db),
    _=Depends(auth_api.get_current_active_user),
):
    return await tweet_api.get_all_tweets(db)


@router.post(
    "/tweets",
    response_model=tweet_schema.TweetCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    tweet_body: tweet_schema.TweetCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    return await tweet_api.create_tweet(db, current_user, tweet_body)


@router.get(
    "/tweets/{tweet_id}",
    response_model=tweet_schema.Tweet,
    status_code=status.HTTP_200_OK,
)
async def get_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(auth_api.get_current_active_user),
):
    tweet = await tweet_api.find_by_id(db, tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet: {tweet_id} Not Found"
        )
    return tweet


@router.patch(
    "/tweets/{tweet_id}",
    response_model=tweet_schema.Tweet,
    status_code=status.HTTP_200_OK,
)
async def update_tweet(
    tweet_id: int,
    tweet_body: tweet_schema.TweetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    updated = await tweet_api.find_by_id(db, tweet_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet: {tweet_id} Not Found"
        )

    if updated.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Authenticated"
        )

    return await tweet_api.update_tweet(db, updated, tweet_body)


@router.delete(
    "/tweets/{tweet_id}", response_model=None, status_code=status.HTTP_200_OK
)
async def delete_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    tweet: tweet_model.Tweet | None = await tweet_api.find_by_id(db, tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet: {tweet_id} Not Found"
        )

    if tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )

    return await tweet_api.delete_tweet(db, tweet)
