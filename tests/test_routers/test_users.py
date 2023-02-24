import pytest
from fastapi import status

from api.schemas import users as user_schema
from tests.factories import UserFactory, create_access_token
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetUser:
    async def test_get_all_when_not_loggin(self, client):
        resp = await client.get("/users")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_all_users_when_no_users(self, client):
        user = UserFactory.create_user()
        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        resp = await client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

    async def test_get_all_users(self, client):
        for _ in range(9):
            user = UserFactory.create_user()
            resp = await client.post(
                "/users",
                json={"name": user.name, "password": user.password},
            )

        user = UserFactory.create_user()
        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        resp = await client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 10

    async def test_get_user_by_id(self, client):
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        user_id = resp.json()["id"]

        resp = await client.get(f"/users/{user_id}")
        assert resp.status_code == status.HTTP_200_OK

        created = user_schema.UserCreateResponse(**resp.json())
        assert created.name == user.name

    async def test_get_user_by_id_which_doesnt_exist(self, client):
        resp = await client.get(f"/users/12345")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "User:12345 Not Found"}


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


@pytest.mark.asyncio
class TestPatchUser:
    async def test_update_user(self, client):
        # create
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})

        assert resp.json()["name"] == user.name

        # login
        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        # update
        updated_data = {"name": "updated :^)", "password": ""}
        resp = await client.patch("/users", json=updated_data, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["name"] != user.name
        assert resp_obj["name"] == "updated :^)"

    async def test_update_user_invalid_updated_data(self, client):
        # create
        user = UserFactory.create_user()
        await client.post("/users", json={"name": user.name, "password": user.password})

        # login
        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        # update with no name and password
        updated_data = {}
        resp = await client.patch("/users", json=updated_data, headers=headers)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_update_user_when_update_user_access_token_need_recreated(self, client):
        user = UserFactory.create_user()
        await client.post("/users", json={"name": user.name, "password": user.password})

        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        # update
        resp = await client.patch("/users", json={"name": "a", "password": "b"}, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        # When user information is updated, token information is also updated
        # and the user is automatically logged out.
        resp = await client.patch("/users", json={"name": "a", "password": "b"}, headers=headers)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
class TestDeleteUser:
    async def test_delete_user(self, client):
        # create
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

        # login
        await client.post("/users", json={"name": user.name, "password": user.password})
        headers = await create_access_token(client, user.name, user.password)

        # delete
        resp = await client.delete("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_delete_user_with_not_logging(self, client):
        # delete
        resp = await client.delete("/users")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
