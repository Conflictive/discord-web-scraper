"""
database.init_db.py
~~~~~~~~~~~
Script to generate database tables

Dependencies:
    - models: Defines SQLAlchemy ORM models.
    - config: Provides Base and engine used to create tables.
"""

import database.models
from database.config import Base, engine
import asyncio


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
