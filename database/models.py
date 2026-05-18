"""
models.py
~~~~~~~~~~
This module is for creating the tables for the database

Dependencies:
    -
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from config import Base


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User ID:{self.id} Username: {self.username}"
