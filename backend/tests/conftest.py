from typing import Tuple

import pytest

from api.models import users as user_model
from api.schemas import auths as auth_schema
from tests.factories import random_string
from tests.init_async_client import async_client as client


@pytest.fixture
@pytest.mark.asyncio
async def login_fixture(client) -> Tuple[user_model.User, dict]:
    """login_fixture
    create user and login by the created user

    Args:
        None {}: 'client' is not args. fixture 'client' is used automatically

    Returns:
        Tuple {user: user_model.User, headers: dict[str: str]}

        user is a sqlalchemy model instance. see api/models/users.py
        headers is dict like {"Authorization": "Bearer eyj....."}
    """
    user = user_model.User(name=random_string(), password=random_string())
    resp = await client.post("/users", json={"name": user.name, "password": user.password})
    user.id = resp.json()["id"]

    resp = await client.post(
        "/token",
        data={"username": user.name, "password": user.password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    token = auth_schema.TokenData(**resp.json())
    headers = {"Authorization": f"Bearer {token.access_token}"}

    return user, headers
