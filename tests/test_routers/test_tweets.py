import pytest
from fastapi import status

from api.schemas import tweets as tweet_schema
from tests.factories import UserFactory, create_access_token, random_string
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllTweet:
    async def test_get_all_tweets_but_empty(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.get("/tweets", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_get_all_tweets(self, client, login_fixture):
        _, headers = await login_fixture

        for _ in range(5):
            await client.post("/tweets", json={"tweet": random_string()}, headers=headers)

        resp = await client.get("/tweets", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 5


@pytest.mark.asyncio
class TestPostTweet:
    async def test_post_tweet(self, client, login_fixture):
        user, headers = await login_fixture

        resp = await client.post("/tweets", json={"tweet": "my first tweet"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        tweet = tweet_schema.TweetCreateResponse(**resp.json())
        assert tweet.tweet == "my first tweet"

    async def test_post_tweet_which_has_invalid_request_body(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/tweets", json={"spam": "Why I stay woke up?"}, headers=headers)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
