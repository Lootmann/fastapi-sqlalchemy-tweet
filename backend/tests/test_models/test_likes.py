from api.models.likes import Like


def test_like_model_repr():
    like = Like(id=1, user_id=1, tweet_id=1)
    assert str(like) == "<Like (id, user_id, tweet_id) = (1, 1, 1)>"
