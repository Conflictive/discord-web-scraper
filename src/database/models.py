"""Defines the layout of the tables in the database.

Dependencies:
    - SQLAlchemy: `Mapped`, `mapped_column`, and SQL types used to define ORM models.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """Tracks all users that have interacted with the bot.

    Attributes:
        discord_id: The primary key identifier assigned by discord.
        username: The username of the user

    """

    __tablename__ = "users"

    # Columns
    discord_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User ID:{self.discord_id} Username: {self.username}"

    # Relationships
    # A user can have many subscriptions
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="user")


class Champion(Base):
    """Tracks all champions that exist within the game.

    This table stores every champion that is within the game obtained from the LoL API,

    Attributes:
        id: The primary key identifier assigned by Riot.
        name: The name of the champion.
        search_name: A cleaned version of the name to make comparison easier.
    """

    __tablename__ = "champions"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    search_name: Mapped[str] = mapped_column(String, index=True)

    # Relationships
    # A champion can have many skins
    skins: Mapped[list["Skin"]] = relationship(back_populates="champion")

    def __repr__(self) -> str:
        return f"<Champion:{self.name}>"


class Skin(Base):
    """Tracks all skins that exist within the game.

    This table stores every skin that is within the game obtained from the LoL API,
    it links skins directly to the champions registry table
    via unique foreign key relations.

    Attributes:
        id: The primary key identifier assigned by Riot.
        name: The name of the skin.
        search_name: A cleaned version of the name to make comparison easier.
        champion_id: Foreign key reference linking to the champions table.
    """

    __tablename__ = "skins"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    search_name: Mapped[str] = mapped_column(String, index=True)

    # Foreign Keys
    champion_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("champions.id"), nullable=False
    )

    # Relationships
    # A skin can have many subscriptions
    # Skins have one champion they belong to
    # Skins have multiple sales
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="skin")
    champion: Mapped["Champion"] = relationship(back_populates="skins")
    sales: Mapped[list["SkinSale"]] = relationship(back_populates="skin")

    def __repr__(self) -> str:
        return f"<Skin:{self.name}>"


class Subscription(Base):
    """Tracks active subscriptions from users for specific skins.

    This table stores the subscription data of users that have subscribed to a skin,
    linking a subscription to its user and their skin via unique foreign key relations.

    Attributes:
        id: The auto-incrementing primary key identifier.
        user_id: Foreign key reference linking to the users table.
        skin_id: Foreign key reference linking to the skins registry.
    """

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


class SkinSale(Base):
    """Tracks active and historical League of Legends skin discounts.

    This table stores the pricing data scraped from an external website ,
    linking web-scraped sale entries directly to the skins inventory table
    via unique foreign key relations.

    Attributes:
        id: The auto-incrementing primary key identifier.
        skin_id: Foreign key reference linking to the master skins registry.
        sale_price: The active discounted price in Riot Points (RP).
        original_price: The base retail price of the skin before markdown.
        start_data: Timestamp indicating when the sale pricing began.
        end_date: Timestamp indicating when the sale pricing expires.
    """

    __tablename__ = "skin_sales"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    skin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skins.id", ondelete="CASCADE"), nullable=False
    )

    # Pricing data
    sale_price: Mapped[int] = mapped_column(Integer, nullable=False)
    original_price: Mapped[int] = mapped_column(Integer, nullable=False)

    # Dates to determine what is currently on sale and what was on sale
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    # A sale has multiple skins
    skin: Mapped["Skin"] = relationship(back_populates="sales")
