import pytest
from fastapi import status

from api.schemas import users as user_schema
from tests.factories import UserFactory
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestCreateToken:
    async def test_login_and_create_valid_token(self, client):
        # create user
        user: user_schema.UserCreateResponse = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

        # login
        resp = await client.post(
            "/token",
            data={"username": user.name, "password": user.password},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access_token" in resp.json()
        assert "token_type" in resp.json()


@pytest.mark.asyncio
class TestLogin:
    async def test_try_to_login_with_invalid_user_info(self, client):
        # create user
        user: user_schema.UserCreate = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

        # login by wrong name
        resp = await client.post(
            "/token",
            data={"username": user.name, "password": "moge"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # login by wrong password
        resp = await client.post(
            "/token",
            data={"username": "hogehoge", "password": user.password},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # login by wrong both
        resp = await client.post(
            "/token",
            data={"username": "hogehoge", "password": "mogera"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND
