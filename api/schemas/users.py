from typing import List

from pydantic import BaseModel, Field

from api.schemas.tweets import Tweet


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str = Field("")
    password: str = Field("")

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class UserCreateResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    tweets: List[Tweet]

    class Config:
        orm_mode = True
