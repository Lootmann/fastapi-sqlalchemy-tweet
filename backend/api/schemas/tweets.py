from pydantic import BaseModel


class TweetBase(BaseModel):
    message: str

    class Config:
        orm_mode = True


class TweetCreate(TweetBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "message": "new tweet :^)",
            }
        }


class TweetCreateResponse(TweetBase):
    id: int


class TweetUpdate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    user_id: int
