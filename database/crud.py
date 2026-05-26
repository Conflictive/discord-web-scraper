"""
database.crud.py
~~~~~~~~
Database module for all CRUD operations
"""

from database.config import engine, AsyncSessionLocal
import database.models as models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert


async def bulk_db_write(models_class, data):
    """
    Writes bulk data (lists) to the database

    Args:
        models_class(DeclarativeBase): Class to target the destination table
        data (List[dict]): A list of dictionaries containing the necessary keys for the given class
    """
    # Duplicates are ignored whilst new data is written

    async with AsyncSessionLocal() as session:
        statement = insert(models_class)

        if hasattr(models_class, "name"):
            statement = statement.on_conflict_do_nothing(index_elements=["name"])

        await session.execute(statement, data)
        await session.commit()


async def get_all_from_table(models_class):
    """
    Gets all records from a specified database table and flattens them into a clean list.

    Args:
        models_class (DeclarativeBase): Class to target the relevant table

    Returns:
        list: list containing SQLAlchemy model objects
    """
    statement = select(models_class)

    async with AsyncSessionLocal() as session:
        result = await session.execute(statement)

        return result.scalars().all()


async def get_skin_name_to_id_map():
    """Fetches all skins once and returns a dict mapping {name: id}"""

    async with AsyncSessionLocal() as session:
        statement = select(models.Skin.name, models.Skin.id)
        result = await session.execute(statement)
        return dict(result.all())


async def get_active_sales_with_skins():
    """Fetches all sales and loads their connected skin models."""
    async with AsyncSessionLocal() as session:
        statement = select(models.SkinSale).options(selectinload(models.SkinSale.skin))

        result = await session.execute(statement)
        return result.scalars().all()
