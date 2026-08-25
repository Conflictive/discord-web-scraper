from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    autoflush=False, bind=engine, expire_on_commit=False
)
