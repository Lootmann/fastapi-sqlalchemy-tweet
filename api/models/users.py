from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.likes import Like
from api.models.tweets import Tweet


class User(Base):
    """
    User : Tweet = 1 : n
    User : Like  = 1 : n
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]

    tweets: Mapped[List["Tweet"]] = relationship("Tweet", back_populates="user")
    favorites: Mapped[List["Like"]] = relationship("Like", back_populates="user")

    def __repr__(self) -> str:
        return f"<User (id, name, tweets) = ({self.id}, {self.name}, {self.tweets})>"
