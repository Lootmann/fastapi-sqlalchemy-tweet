from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)

    # (Favorite:User) = (n:1)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="favorites")

    # (Favorite:Tweet) = (n:1)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))
    tweet = relationship("Tweet", back_populates="favorites")

    def __repr__(self) -> str:
        return f"<Favorite (id, user_id, tweet_id) = ({self.id}, {self.user_id}, {self.tweet_id})>"
