from typing import List

from pydantic import BaseModel, Field, validator


class FavoriteBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class FavoriteCreate(FavoriteBase):
    tweet_id: int = Field(...)


class FavoriteCreateResponse(FavoriteCreate):
    id: int


class Favorite(BaseModel):
    id: int
    user_id: int
    tweet_id: int
