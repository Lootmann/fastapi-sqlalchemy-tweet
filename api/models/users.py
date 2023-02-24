"""api/models/users.py


class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship()
"""
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.tweets import Tweet


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]

    tweets: Mapped[List["Tweet"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User (id, name) = ({self.id}, {self.name})>"
