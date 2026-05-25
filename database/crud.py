"""
database.crud.py
~~~~~~~~
Database module for all CRUD operations
"""

from database.config import engine
import database.models as models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert


async def bulk_db_write(models_class, data):
    """
    Writes bulk data (lists) to the database

    Args:
        models_class(DeclarativeBase): Class to target the destination table
        data (List[dict]): A list of champion dictionaries containing the following keys:
            - name(str): The champion's name
    """
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Duplicates are ignored whilst new data is written
            statement = insert(models_class).on_conflict_do_nothing(
                index_elements=["name"]
            )
            await session.execute(statement, data)
