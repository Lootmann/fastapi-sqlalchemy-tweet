import pytest
from fastapi import status

from api.schemas import users as user_schema
from tests.factories import UserFactory, create_access_token, random_string
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllUsers:
    async def test_get_all_when_not_loggin(self, client):
        resp = await client.get("/users")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_1_user(self, client, login_fixture):
        _, headers = await login_fixture
        resp = await client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

    async def test_get_2_users(self, client, login_fixture):
        _, headers = await login_fixture

        user = UserFactory.create_user()
        await client.post(
            "/users", json={"name": user.name, "password": user.password}, headers=headers
        )

        resp = await client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 2

    async def test_get_all_users(self, client):
        for _ in range(4):
            await client.post(
                "/users",
                json={"name": random_string(), "password": random_string()},
            )

        user = UserFactory.create_user()
        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        resp = await client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 5


@pytest.mark.asyncio
class TestGetUser:
    async def test_get_one_user(self, client, login_fixture):
        user, headers = await login_fixture

        resp = await client.get(f"/users/{user.id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        user_response = user_schema.User(**resp.json())
        assert user_response.id == user.id
        assert user_response.name == user.name
        assert user_response.tweets == user.tweets

    async def test_get_one_user_which_is_wrong_id(self, client, login_fixture):
        user, headers = await login_fixture

        resp = await client.get(f"/users/{user.id + 1000}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestPostUser:
    async def test_post_user(self, client):
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_post_many_users(self, client):
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_post_dulicate_user_name(self, client):
        user = UserFactory.create_user()

        await client.post("/users", json={"name": user.name, "password": user.password})
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_409_CONFLICT
        assert resp.json() == {"detail": f"Duplicate Username: {user.name}"}

    async def test_post_user_with_invalid_field(self, client):
        resp = await client.post("/users", json={"nama": "hoge", "password": "mogege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        resp = await client.post("/users", json={"name": "huge", "secret": "magege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        resp = await client.post("/users", json={"name": "magege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        resp = await client.post("/users", json={"password": "magege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
