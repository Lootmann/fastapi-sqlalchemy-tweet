from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models.favorites import Favorite as FavoriteModel
from api.models.users import User as UserModel
from api.schemas import favorites as favorite_schema


async def get_all_favorites(db: AsyncSession, user_id: int) -> List[FavoriteModel]:
    return (await db.execute(select(FavoriteModel).filter(FavoriteModel.user_id == user_id))).fetchall()


async def find_by_user_id_and_tweet_id(db: AsyncSession, user_id: int, tweet_id: int) -> FavoriteModel:
    fav = await db.execute(
        select(FavoriteModel)
        .filter(FavoriteModel.user_id == user_id)
        .filter(FavoriteModel.tweet_id == tweet_id)
    )
    return fav.first()


async def create_favorite(
    db: AsyncSession, favorite_body: favorite_schema.FavoriteCreate, user: UserModel
) -> FavoriteModel:
    favorite = FavoriteModel(**favorite_body.dict())
    favorite.user_id = user.id

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)

    return favorite


async def delete_favorite(db: AsyncSession, favorite_model: FavoriteModel) -> None:
    db.delete(favorite_model)
    await db.commit()
    return
