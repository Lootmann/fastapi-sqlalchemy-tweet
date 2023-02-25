from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.tweets import Tweet


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))

    def __repr__(self) -> str:
        return f"<Favorite (id, user_id, tweet_id) = ({self.id}, {self.user_id}, {self.tweet_id})>"