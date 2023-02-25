import pytest
from fastapi import status

from api.schemas import tweets as tweet_schema
from api.schemas import users as user_schema
from tests.factories import (
    TweetFactory,
    UserFactory,
    create_access_token,
    random_string,
)
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllFavorites:
    async def test_get_all_favorites_but_empty(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.get("/favorites", headers=headers)
        assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestPostFavorites:
    async def test_create_favorite(self, client, login_fixture):
        _, headers = await login_fixture

        tweet_body = TweetFactory.gen_tweet()
        resp = await TweetFactory.create_tweet(client, headers, tweet_body)

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["message"] == tweet_body.message
