from api.models.likes import Like
from api.models.tweets import Tweet
from api.models.users import User


def test_tweet_model_repr():
    user = User(id=1, name="guest", password="=-2mcb6720-k")
    likes = [
        Like(id=1, user_id=1, tweet_id=1),
        Like(id=2, user_id=2, tweet_id=1),
    ]
    tweet = Tweet(id=1, message="hello world", user_id=user.id, likes=likes)

    assert str(tweet) == "<Tweet (id, message, user_id) = (1, hello world, 1)>"
