import pytest
from fastapi import status

from api.schemas import tweets as tweet_schema
from api.schemas import users as user_schema
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
        await client.post("/tweets", json={"tweet": "second tweet"}, headers=headers)

        tweet = tweet_schema.TweetCreateResponse(**resp.json())
        assert tweet.tweet == "my first tweet"

        # check user-tweet relation
        resp = await client.get("/users", headers=headers)
        user_obj = user_schema.User(**resp.json()[0])

        assert user_obj.id == user.id
        assert len(user_obj.tweets) == 2
        assert user_obj.tweets[0].tweet == "my first tweet"
        assert user_obj.tweets[1].tweet == "second tweet"

    async def test_post_tweet_which_has_invalid_request_body(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post(
            "/tweets", json={"spam": "How do I stay wokewoke up?"}, headers=headers
        )
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestGetTweet:
    async def test_get_tweet(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/tweets", json={"tweet": "first post"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        tweet_id = resp.json()["id"]

        # get tweet
        resp = await client.get(f"/tweets/{tweet_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        tweet = tweet_schema.Tweet(**resp.json())
        assert tweet.tweet == "first post"

    async def test_get_tweet_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        # get tweet
        resp = await client.get(f"/tweets/123", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Tweet: 123 Not Found"}
