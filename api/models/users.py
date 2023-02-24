from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.tweets import Tweet


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]

    tweets: Mapped[List[Tweet]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User (id, name, tweets) = ({self.id}, {self.name}, {self.tweets})>"
