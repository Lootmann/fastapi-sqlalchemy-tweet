from api.models import tweets as tweet_model
from api.models import users as user_model


def test_user_model_repr():
    user = user_model.User(id=1, name="hoge", password="9akldsjf9")
    assert str(user) == f"<User (id, name, tweets) = ({user.id}, {user.name}, [])>"


def test_user_model_repr_with_tweet():
    user = user_model.User(id=1, name="hoge", password="9akldsjf9")
    tweet = tweet_model.Tweet(id=1, tweet="hoge", user_id=user.id)
    user.tweets.append(tweet)
    assert str(user) == f"<User (id, name, tweets) = ({user.id}, {user.name}, [<Tweet 1: hoge>])>"
