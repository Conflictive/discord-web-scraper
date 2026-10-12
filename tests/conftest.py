import os
import urllib.parse

import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

import src.database.models as models
from src.database.models import Base
from src.database.session import AsyncSessionLocal

load_dotenv()

db_url = os.environ.get("TEST_DB_URL")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_pass = urllib.parse.quote_plus(db_pass)

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_url}"


def get_test_engine():
    """Generates an engine instance."""
    return create_async_engine(
        DATABASE_URL,
        pool_reset_on_return=None,  # Prevents pool cleanups from hanging async loops
    )


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    """Sets up a test db."""
    engine = get_test_engine()

    AsyncSessionLocal.configure(bind=engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    yield


@pytest_asyncio.fixture(scope="function")
async def db_session(setup_database):
    """Create and yields a session for the db."""
    async with AsyncSessionLocal() as session:
        yield session


# Add preset champions to test database so skins can be added and tested
@pytest_asyncio.fixture(scope="function")
async def seed_champion(db_session):
    """Seeds a single champion into the test DB so skins have a parent row."""
    champion = models.Champion(id=33, name="Rammus", search_name="rammus")
    db_session.add(champion)
    await db_session.commit()

    return champion


@pytest_asyncio.fixture(scope="function")
async def seed_skin(db_session, seed_champion):
    """Seeds a skin into the test db for subscription testing."""
    skin = models.Skin(
        id=330001, name="King Rammus", search_name="kingrammus", champion_id=33
    )
    db_session.add(skin)
    await db_session.commit()

    return skin


@pytest_asyncio.fixture(scope="function")
async def seed_user(db_session):
    """Seeds a single user into the test DB for subscription operations."""
    user = models.User(discord_id=1022, username="Test_User")
    db_session.add(user)
    await db_session.commit()

    return user
