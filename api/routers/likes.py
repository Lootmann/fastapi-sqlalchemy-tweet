from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import auths as auth_api
from api.cruds import likes as like_api
from api.cruds import tweets as tweet_api
from api.cruds import users as user_api
from api.db import get_db
from api.schemas import likes as like_schema
from api.schemas import tweets as tweet_schema
from api.schemas import users as user_schema

router = APIRouter(tags=["likes"])


@router.get("/likes", response_model=List[like_schema.Like], status_code=status.HTTP_200_OK)
async def get_all_likes(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    """get all likes by login user"""
    results = await like_api.get_all_likes(db, current_user.id)
    return [r[0] for r in results]


@router.get(
    "/users/{user_id}/likes/tweets",
    response_model=List[tweet_schema.Tweet],
    status_code=status.HTTP_200_OK,
)
async def get_all_tweets_which_user_likes(user_id: int, db: AsyncSession = Depends(get_db)):
    tweets = await tweet_api.get_all_tweets_which_user_likes(db, user_id)
    return [u[0] for u in tweets]


@router.post(
    "/tweets/{tweet_id}/likes",
    response_model=like_schema.LikeCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_like(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    like = await like_api.find_by_user_id_and_tweet_id(db, current_user.id, tweet_id)
    if like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already like this tweet.")

    tweet = await tweet_api.find_by_id(db, tweet_id)
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet: {tweet_id} Not Found")

    return await like_api.create_like(db, tweet, current_user)


@router.delete("/tweets/{tweet_id}/likes", response_model=None, status_code=status.HTTP_200_OK)
async def delete_like(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    like = await like_api.find_by_user_id_and_tweet_id(db, current_user.id, tweet_id)
    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tweet: {tweet_id} is not liked by you"
        )
    return await like_api.delete_like(db, like)
