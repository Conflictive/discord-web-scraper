"""
models.py
~~~~~~~~~~
This module is for creating the tables for the database

Dependencies:
    - SQLAlchemy: `Mapped`, `mapped_column`, and SQL types used to define ORM models.
    - config: Exposes `Base` (DeclarativeBase) used as the model base class.
"""

from sqlalchemy import Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config import Base
from __future__ import annotations


class User(Base):
    __tablename__ = "users"

    # Columns
    discord_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User ID:{self.id} Username: {self.username}"

    # Relationships
    # A user can have many subscriptions
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="user")


class Champion(Base):
    __tablename__ = "champions"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relationships
    # A champion can have many skins
    skins: Mapped[list["Skin"]] = relationship(back_populates="champion")

    def __repr__(self) -> str:
        return f"<Champion:{self.name}>"


class Skin(Base):
    __tablename__ = "skins"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Foreign Keys
    champion_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("champion.id"), nullable=False
    )

    # Relationships
    # A skin can have many subscriptions
    # Skins have one champion they belong to
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="skin")
    champion: Mapped["Champion"] = relationship(back_populates="skins")

    def __repr__(self) -> str:
        return f"<Skin:{self.name}>"


class Subscription(Base):
    __tablename__ = "subscriptions"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.discord_id", ondelete="CASCADE"), nullable=False
    )
    skin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skins.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    # User can have many subscriptions
    # Skin can have many subscriptions
    user: Mapped["User"] = relationship(back_populates="subscriptions")
    skin: Mapped["Skin"] = relationship(back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"<Subscription User:{self.user_id} -> Skin:{self.skin_id}>"
