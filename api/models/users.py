from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.favorites import Favorite
from api.models.tweets import Tweet


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]

    # NOTE: (User:Tweet) = (1:n)
    tweets: Mapped[List[Tweet]] = relationship("Tweet", back_populates="user")

    # NOTE: (User:Favorite) = (1:n)
    favorites: Mapped[List[Favorite]] = relationship("Favorite", back_populates="user")

    def __repr__(self) -> str:
        return f"<User (id, name, tweets) = ({self.id}, {self.name}, {self.tweets})>"
