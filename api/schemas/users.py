from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str = Field("")
    password: str = Field("")

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserCreateResponse(UserBase):
    id: int


class User(UserBase):
    id: int
    password: str
