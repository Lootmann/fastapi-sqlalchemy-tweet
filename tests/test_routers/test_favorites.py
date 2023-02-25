import pytest
from fastapi import status

from api.schemas import favorites as favorite_schema
from tests.factories import TweetFactory
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetAllFavorites:
    async def test_get_all_favorites_but_empty(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.get("/favorites", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_get_all_favorites(slef, client, login_fixture):
        _, headers = await login_fixture

        # create tweets and favorite these tweets
        for _ in range(20):
            tweet = TweetFactory.gen_tweet()
            resp = await TweetFactory.create_tweet(client, headers, tweet)

            tweet_id = resp.json()["id"]

            # fav
            resp = await client.post("/favorites", json={"tweet_id": tweet_id}, headers=headers)
            assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.get("/favorites", headers=headers)
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
        resp = await client.post("/favorites", json={"tweet_id": tweet_id}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        fav_response = favorite_schema.FavoriteCreateResponse(**resp.json())
        assert fav_response.tweet_id == tweet_id
