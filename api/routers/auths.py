from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import auths as auth_api
from api.db import get_db
from api.schemas import auths as auth_schema
from api.schemas import users as user_schema
from api.settings import Settings

credential = Settings()
router = APIRouter()


@router.post("/token", response_model=auth_schema.TokenData, status_code=status.HTTP_200_OK)
async def login_user(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    found_user: user_schema.User = await auth_api.authenticate_user(
        db, form_data.username, form_data.password
    )

    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    access_token_expires = timedelta(minutes=credential.access_token_expire_minutes)
    data = {"sub": found_user.name}
    access_token = await auth_api.create_access_token(data, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
