"""api/models/tweets.py

SQLAlchemy Official Relationships

- https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]

    # NOTE: (Tweet:User) = (n:1)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="tweets")

    # NOTE: (Tweet:Favote) = (1:n)
    favorites: Mapped["Favorite"] = relationship("Favorite", back_populates="tweet")

    def __repr__(self) -> str:
        return f"<Tweet (id, message, user_id) = ({self.id}, {self.message}, {self.user_id})>"
