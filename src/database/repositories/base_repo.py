"""Handles all generic asynchronous CRUD operations for the application database."""

from typing import Any, Sequence, Type

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


async def bulk_db_write(
    session: AsyncSession,
    model_class: Type[DeclarativeBase],
    data: list[dict[str, Any]],
) -> None:
    """Writes bulk data lists to the database whilst ignoring duplicates.

    Args:
        session: Active request-scoped database session.
        model_class: Class to target the destination table.
        data: A list of dictionaries containing the necessary keys for the given class.
    """
    statement = insert(model_class)

    if hasattr(model_class, "name"):
        statement = statement.on_conflict_do_nothing(index_elements=["name"])

    await session.execute(statement, data)
    await session.commit()


async def get_all_from_table(
    session: AsyncSession,
    model_class: Type[DeclarativeBase],
) -> Sequence[DeclarativeBase]:
    """Gets all records from a database table then flattens them into a clean list.

    Args:
        session: Active request-scoped database session.
        model_class: Class to target the relevant table.

    Returns:
        A sequence containing the fetched SQLAlchemy live model objects.
    """
    statement = select(model_class)
    result = await session.execute(statement)

    return result.scalars().all()
