from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import auths as auth_api
from api.cruds import favorites as favorite_api
from api.db import get_db
from api.models import favorites as favorite_model
from api.schemas import favorites as favorite_schema

router = APIRouter()


@router.get("/favorites", response_model=List[favorite_schema.Favorite], status_code=status.HTTP_200_OK)
async def get_all_favorites(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    results = await favorite_api.get_all_favorites(db, current_user.id)
    return [r[0] for r in results]


@router.post(
    "/favorites", response_model=favorite_schema.FavoriteCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_favorite(
    favorite_body: favorite_schema.FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    return await favorite_api.create_favorite(db, favorite_body, current_user)
