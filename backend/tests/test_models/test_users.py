from api.models import likes as like_model
from api.models import tweets as tweet_model
from api.models import users as user_model


def test_user_model_repr():
    user = user_model.User(id=1, name="hoge", password="9akldsjf9")
    assert (
        str(user)
        == f"<User (id, name, tweets, likes) = ({user.id}, {user.name}, [], [])>"
    )


def test_user_model_repr_with_tweet():
    user = user_model.User(id=1, name="hoge", password="9akldsjf9")
    tweet = tweet_model.Tweet(id=1, message="hoge", user_id=user.id)
    user.tweets.append(tweet)
    tweet_str = "<Tweet (id, message, user_id) = (1, hoge, 1)>"

    assert (
        str(user) == f"<User (id, name, tweets, likes) = (1, hoge, [{tweet_str}], [])>"
    )


def test_user_model_rep_with_tweet_and_like():
    user = user_model.User(id=1, name="hoge", password="9akldsjf9")
    tweet = tweet_model.Tweet(id=1, message="hoge", user_id=user.id)
    user.tweets.append(tweet)

    like = like_model.Like(id=1, user_id=1, tweet_id=1)
    user.likes.append(like)

    tweet_str = "<Tweet (id, message, user_id) = (1, hoge, 1)>"
    like_str = "<Like (id, user_id, tweet_id) = (1, 1, 1)>"

    assert (
        str(user)
        == f"<User (id, name, tweets, likes) = (1, hoge, [{tweet_str}], [{like_str}])>"
    )
