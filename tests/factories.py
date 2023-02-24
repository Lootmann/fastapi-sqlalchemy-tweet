from random import choice, randint
from string import ascii_letters

from api.schemas import users as user_schema


def random_string(min_: int = 5, max_: int = 20) -> str:
    return "".join(choice(ascii_letters) for _ in range(randint(min_, max_)))


async def create_access_token(client, username: str, password: str):
    resp = await client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    access_token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


class UserFactory:
    @staticmethod
    def create_user() -> user_schema.UserCreate:
        username, password = random_string(), random_string()
        return user_schema.UserCreate(name=username, password=password)
