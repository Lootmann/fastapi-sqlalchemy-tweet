"""api/models/tweets.py

SQLAlchemy Official Relationships

- https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

"""
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.favorites import Favorite


class Tweet(Base):
    """
    Tweet : User = n : 1
    Tweet : Fav  = 1 : n
    """

    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="tweets")

    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="tweet")

    def __repr__(self) -> str:
        return f"<Tweet (id, message, user_id) = ({self.id}, {self.message}, {self.user_id})>"
