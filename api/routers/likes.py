from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import auths as auth_api
from api.cruds import likes as like_api
from api.db import get_db
from api.schemas import likes as like_schema

router = APIRouter()


@router.get("/likes", response_model=List[like_schema.Like], status_code=status.HTTP_200_OK)
async def get_all_likes(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    results = await like_api.get_all_likes(db, current_user.id)
    return [r[0] for r in results]


@router.post(
    "/tweets/{tweet_id}/likes",
    response_model=like_schema.LikeCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_like(
    tweet_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(auth_api.get_current_active_user)
):
    return await like_api.create_like(db, tweet_id, current_user)


@router.delete("/tweets/{tweet_id}/likes", response_model=None, status_code=status.HTTP_200_OK)
async def delete_like(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    like = await like_api.find_by_user_id_and_tweet_id(db, current_user.id, tweet_id)
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like Not Found")
    return await like_api.delete_like(db, like)
