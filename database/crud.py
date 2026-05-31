"""Handles all generic asynchronous CRUD operations for the application database.

This module provides reusable database utilities to prevent code
duplication across different model tables
"""

from typing import Any, Sequence, Type

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase

from database.config import AsyncSessionLocal


async def bulk_db_write(
    model_class: Type[DeclarativeBase], data: list[dict[str:Any]]
) -> None:
    """Writes bulk data lists to the database whilst ignoring duplicates.

    Args:
        model_class: Class to target the destination table
        data: A list of dictionaries containing the necessary keys for the given class
    """
    async with AsyncSessionLocal() as session:
        statement = insert(model_class)

        if hasattr(model_class, "name"):
            statement = statement.on_conflict_do_nothing(index_elements=["name"])

        await session.execute(statement, data)
        await session.commit()


async def get_all_from_table(
    model_class: Type[DeclarativeBase],
) -> Sequence[DeclarativeBase]:
    """Gets all records from a database table then flattens them into a clean list.

    Args:
        model_class: Class to target the relevant table

    Returns:
        A sequence containing the fetched SQLAlchemy live model objects.
    """
    statement = select(model_class)

    async with AsyncSessionLocal() as session:
        result = await session.execute(statement)

        return result.scalars().all()
