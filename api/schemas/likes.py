from pydantic import BaseModel


class LikeBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class LikeCreateResponse(LikeBase):
    id: int
    tweet_id: int


class Like(LikeBase):
    id: int
    user_id: int
    tweet_id: int
