from pydantic import BaseModel


class TweetBase(BaseModel):
    tweet: str

    class Config:
        orm_mode = True


class TweetCreate(TweetBase):
    pass


class TweetCreateResponse(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    user_id: int
