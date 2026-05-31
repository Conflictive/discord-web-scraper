"""Generates the initial relational database tables schema within PostgreSQL."""

import asyncio

import database.models  # noqa: F401
from database.config import Base, engine


async def init_db() -> None:
    """Creates all registered database tables inside the active database engine."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
