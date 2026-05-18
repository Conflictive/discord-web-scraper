"""
models.py
~~~~~~~~~~
This module is for creating the tables for the database

Dependencies:
    - SQLAlchemy: `Mapped`, `mapped_column`, and SQL types used to define ORM models.
    - config: Exposes `Base` (DeclarativeBase) used as the model base class.
"""

from sqlalchemy import Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from config import Base


class User(Base):
    __tablename__ = "users"

    discord_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User ID:{self.id} Username: {self.username}"


class Champion(Base):
    __tablename__ = "champions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Champion:{self.name}>"


class Skin(Base):
    __tablename__ = "skins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Skin:{self.name}>"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.discord_id", ondelete="CASCADE"), nullable=False
    )
    skin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skins.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Subscription User:{self.user_id} -> Skin:{self.skin_id}>"
