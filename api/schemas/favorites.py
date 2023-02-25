from pydantic import BaseModel, Field


class FavoriteBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class FavoriteCreate(FavoriteBase):
    tweet_id: int = Field(...)


class FavoriteCreateResponse(FavoriteCreate):
    id: int


class FavoriteDelete(FavoriteCreate):
    pass


class Favorite(FavoriteBase):
    id: int
    user_id: int
    tweet_id: int
