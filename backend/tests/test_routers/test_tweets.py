import pytest
from fastapi import status

from api.schemas import tweets as tweet_schema
from api.schemas import users as user_schema
from tests.factories import TweetFactory, UserFactory, create_access_token
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
            tweet = TweetFactory.gen_tweet()
            await TweetFactory.create_tweet(client, headers, tweet)

        resp = await client.get("/tweets", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 5


@pytest.mark.asyncio
class TestPostTweet:
    async def test_post_tweet(self, client, login_fixture):
        user, headers = await login_fixture

        resp = await client.post("/tweets", json={"message": "my first tweet"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED
        await client.post("/tweets", json={"message": "second tweet"}, headers=headers)

        tweet = tweet_schema.TweetCreateResponse(**resp.json())
        assert tweet.message == "my first tweet"

        # check user-tweet relation
        resp = await client.get("/users", headers=headers)
        user_obj = user_schema.User(**resp.json()[0])

        assert user_obj.id == user.id
        assert len(user_obj.tweets) == 2
        assert user_obj.tweets[0].message == "my first tweet"
        assert user_obj.tweets[1].message == "second tweet"

    async def test_post_tweet_which_has_invalid_request_body(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/tweets", json={"spam": "How do I stay wokewoke up?"}, headers=headers)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestGetTweet:
    async def test_get_tweet(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/tweets", json={"message": "first post"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        tweet_id = resp.json()["id"]

        # get tweet
        resp = await client.get(f"/tweets/{tweet_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        tweet = tweet_schema.Tweet(**resp.json())
        assert tweet.message == "first post"

    async def test_get_tweet_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        # get tweet
        resp = await client.get(f"/tweets/123", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Tweet: 123 Not Found"}


@pytest.mark.asyncio
class TestUpdateTweet:
    async def test_update_tweet(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/tweets", json={"message": "first post"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        tweet_id = resp.json()["id"]

        # update patch
        resp = await client.patch(f"/tweets/{tweet_id}", json={"message": "updated"}, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        tweet = tweet_schema.Tweet(**resp.json())
        assert tweet.id == tweet_id
        assert tweet.message == "updated"

    async def test_update_tweet_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.patch(f"/tweets/12345", json={"message": "updated"}, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Tweet: 12345 Not Found"}

    async def test_update_tweet_when_not_author(self, client, login_fixture):
        user, headers = await login_fixture

        resp = await client.post("/tweets", json={"message": "first post"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        tweet_id = resp.json()["id"]

        # create new user
        new_user = UserFactory.gen_user()
        assert user.name != new_user.name
        assert user.password != new_user.password

        await UserFactory.create_user(client, new_user)
        new_headers = await create_access_token(client, new_user.name, new_user.password)

        # update tweet
        resp = await client.patch(
            f"/tweets/{tweet_id}", json={"message": "updated new user"}, headers=new_headers
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestDeleteTweet:
    async def test_delete_tweet(self, client, login_fixture):
        _, headers = await login_fixture

        tweet = TweetFactory.gen_tweet()
        resp = await TweetFactory.create_tweet(client, headers, tweet)
        assert resp.status_code == status.HTTP_201_CREATED

        # keep original tweet
        original_tweet = tweet_schema.TweetCreateResponse(**resp.json())

        resp = await client.get("/tweets", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        # delete
        resp = await client.delete(f"/tweets/{original_tweet.id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp = await client.get("/tweets", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    async def test_try_to_delete_tweet_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.delete(f"/tweets/123", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Tweet: 123 Not Found"}

    async def test_try_to_delete_different_author_tweet(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/tweets", json={"message": "I'm here :^)"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED
        original_tweet = tweet_schema.TweetCreateResponse(**resp.json())

        # create new user
        user = UserFactory.gen_user()
        resp = await UserFactory.create_user(client, user)
        assert resp.status_code == status.HTTP_201_CREATED
        new_headers = await create_access_token(client, user.name, user.password)

        # try to delete tweet by new user
        resp = await client.delete(f"/tweets/{original_tweet.id}", headers=new_headers)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert resp.json() == {"detail": "Not Authorized"}
