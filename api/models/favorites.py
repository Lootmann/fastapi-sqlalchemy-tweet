from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Favorite(Base):
    """
    Fav : User  = n : 1
    Fav : Tweet = n : 1
    """

    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="favorites")

    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="favorites")

    def __repr__(self) -> str:
        return f"<Favorite (id, user_id, tweet_id) = ({self.id}, {self.user_id}, {self.tweet_id})>"
