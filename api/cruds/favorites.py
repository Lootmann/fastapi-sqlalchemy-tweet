from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models import favorites as favorite_model
from api.models import users as user_model
from api.schemas import favorits as favorite_schema


async def get_all_favorites(db: AsyncSession, user_id) -> List[favorite_schema.Favorite]:
    favorites = await db.execute(select(favorite_model.Favorite).filter_by(user_id=user_id))
    return favorites.all()


async def create_favorite(
    db: AsyncSession, favorite_body: favorite_schema.FavoriteCreate, user: user_model.User
) -> favorite_model.Favorite:
    favorite = favorite_model.Favorite(**favorite_body.dict())
    favorite.user_id = user.id

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)

    return favorite