from typing import List

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator

from api.schemas.tweets import Tweet


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """
    name and password are allowed to be empty string.
    when one of them is empty, this Field can't update.
    """

    name: str = Field("", max_length=100)
    password: str = Field("", max_length=100)

    @validator("name")
    def check_name_length(cls, name: str):
        if name == "":
            pass
        else:
            if len(name) < 6:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Username Length should be longer than 6.",
                )
        return name

    @validator("password")
    def check_password_length(cls, password: str):
        if password == "":
            pass
        else:
            if len(password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Password Length should be longer than 6.",
                )
        return password

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str = Field(..., min_length=6, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name": "guest user",
                "password": "hogehoge",
            }
        }


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
