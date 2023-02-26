import pytest
from fastapi import status

from tests.factories import LikeFactory, TweetFactory, UserFactory, create_access_token
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetLikingTweets:
    async def test_get_all_users_which_like_the_tweet(self, client, login_fixture):
        _, headers = await login_fixture

        # create one tweet
        tweet = TweetFactory.gen_tweet()
        resp = await TweetFactory.create_tweet(client, headers, tweet)
        tweet_id = resp.json()["id"]

        # create many user and like the tweet
        for _ in range(10):
            new_user = UserFactory.gen_user()
            resp = await UserFactory.create_user(client, new_user)
            assert resp.status_code == status.HTTP_201_CREATED

            new_headers = await create_access_token(client, new_user.name, new_user.password)
            resp = await client.post(f"/tweets/{tweet_id}/likes", headers=new_headers)
            assert resp.status_code == status.HTTP_201_CREATED

        print("\n>>> test code")
        resp = await client.get(f"/tweets/{tweet_id}/likes/users", headers=headers)
        print(resp.json())
