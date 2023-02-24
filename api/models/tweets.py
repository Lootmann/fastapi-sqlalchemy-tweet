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
    tweet: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tweets")

    def __repr__(self) -> str:
        return f"<Tweet {self.id}: {self.tweet}>"
