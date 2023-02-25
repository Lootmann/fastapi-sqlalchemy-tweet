import pytest
from fastapi import status

from api.schemas import likes as like_schema
from tests.factories import LikeFactory, TweetFactory
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllLikes:
    async def test_get_all_likes_but_empty(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.get("/likes", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_get_all_likes(slef, client, login_fixture):
        _, headers = await login_fixture

        # create tweets and like these tweets
        for _ in range(20):
            tweet = TweetFactory.gen_tweet()
            resp = await TweetFactory.create_tweet(client, headers, tweet)

            tweet_id = resp.json()["id"]

            # fav
            resp = await client.post(f"/tweets/{tweet_id}/likes", headers=headers)
            assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.get("/likes", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 20


@pytest.mark.asyncio
class TestPostFavorites:
    async def test_create_favorite(self, client, login_fixture):
        _, headers = await login_fixture

        tweet_body = TweetFactory.gen_tweet()
        resp = await TweetFactory.create_tweet(client, headers, tweet_body)
        tweet_id = resp.json()["id"]

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["message"] == tweet_body.message

        # favorite == likes
        resp = await client.post(f"/tweets/{tweet_id}/likes", headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        fav_response = like_schema.LikeCreateResponse(**resp.json())
        assert fav_response.tweet_id == tweet_id


@pytest.mark.asyncio
class TestDeleteFavorites:
    async def test_delete_favorite(self, client, login_fixture):
        _, headers = await login_fixture

        tweet_body = TweetFactory.gen_tweet()
        resp = await TweetFactory.create_tweet(client, headers, tweet_body)
        tweet_id = resp.json()["id"]

        # favorite
        resp = await LikeFactory.create_like(client, headers, tweet_id)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.get(f"/tweets/{tweet_id}/likes", headers=headers)
        assert len(resp.json()) == 1

        # delete
        resp = await client.delete(f"/tweets/{tweet_id}/likes", headers=headers)
        print(resp.json())
