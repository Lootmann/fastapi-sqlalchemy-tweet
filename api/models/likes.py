from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Like(Base):
    """
    Like : User  = n : 1
    Like : Tweet = n : 1
    """

    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="likes")

    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="likes")

    def __repr__(self) -> str:
        return f"<Like (id, user_id, tweet_id) = ({self.id}, {self.user_id}, {self.tweet_id})>"
