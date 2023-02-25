from random import choice, randint
from string import ascii_letters

from api.schemas import favorites as favorite_schema
from api.schemas import tweets as tweet_schema
from api.schemas import users as user_schema
from tests.init_async_client import async_client as client


def random_string(min_: int = 6, max_: int = 20) -> str:
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
    def gen_user() -> user_schema.UserCreate:
        username = random_string(min_=6, max_=100)
        password = random_string(min_=6, max_=100)
        return user_schema.UserCreate(name=username, password=password)

    @staticmethod
    async def create_user(client, user_body: user_schema.UserCreate):
        """
        create user with inserting db

        Args:
            client (AsyncSession)
            headers (dict token)     : Bearer JWT Token
            user_body (schema) : {schema.UserCreate}

        Return:
            resp: tweets post response
        """
        return await client.post("/users", json={"name": user_body.name, "password": user_body.password})


class TweetFactory:
    @staticmethod
    def gen_tweet() -> tweet_schema.TweetCreate:
        message = random_string(min_=0, max_=140)
        return tweet_schema.TweetCreate(message=message)

    @staticmethod
    async def create_tweet(client, headers: dict, tweet_body: tweet_schema.TweetCreate):
        """
        create tweet with inserting db

        Args:
            client (AsyncSession)
            headers (dict token) : Bearer JWT Token
            tweet_body (schema)  : TweetCreate schema

        Return:
            resp: tweets post response
        """
        return await client.post("/tweets", json={"message": tweet_body.message}, headers=headers)


class FavoriteFactory:
    @staticmethod
    def gen_favorite(tweet_id: int) -> favorite_schema.FavoriteCreate:
        return favorite_schema.FavoriteCreate(tweet_id=tweet_id)

    @staticmethod
    async def create_favorite(client, headers: dict, favorite_body: favorite_schema.FavoriteCreate):
        """
        create favorite

        Args:
            client (AsyncSession)
            headers (dict token)   : Bearer JWT Token
            favorite_body (schema) : FavoriteCreate schema

        Return:
            resp: favorite post response
        """
        return await client.post("/favorites", json={"tweet_id": favorite_body.tweet_id}, headers=headers)
