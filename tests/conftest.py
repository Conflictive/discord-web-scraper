import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from database.config import Base, AsyncSessionLocal
import database.models as models
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

db_url = os.environ.get("TEST_DB_URL")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_pass = urllib.parse.quote_plus(db_pass)

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_url}"


def get_test_engine():
    """Generates an engine instance"""
    return create_async_engine(
        DATABASE_URL,
        pool_reset_on_return=None,  # Prevents pool cleanups from hanging async loops
    )


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    engine = get_test_engine()

    AsyncSessionLocal.configure(bind=engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    yield


# Add preset champions to test database so skins can be added and tested
@pytest_asyncio.fixture(scope="function")
async def seed_champion(setup_database):
    """Seeds a single champion into the test DB so skins have a parent row."""
    async with AsyncSessionLocal() as session:
        champion = models.Champion(id=33, name="Rammus")
        session.add(champion)
        await session.commit()

        return champion
