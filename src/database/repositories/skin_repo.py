"""Module for handling all CRUD operations that are relevant to skins."""

import re
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import src.database.models as models


async def get_skin_name_to_id_map(session: AsyncSession) -> dict[str, int]:
    """Fetches all skins once and returns a dict mapping {name: id}.

    Args:
        session: Active request-scoped database session.

    Returns:
        dict[str, int]: in the format {name: id} ({Rammus: 33})
    """
    statement = select(models.Skin.name, models.Skin.id)
    result = await session.execute(statement)
    return dict(result.all())


async def get_active_sales_with_skins(
    session: AsyncSession,
) -> Sequence[models.SkinSale]:
    """Fetches all sales and loads their connected skin models.

    Args:
        session: Active request-scoped database session.

    Returns:
        Sequence[models.SkinSale]: Fetched SkinSale model instances with skins loaded.
    """
    statement = select(models.SkinSale).options(selectinload(models.SkinSale.skin))

    result = await session.execute(statement)
    return result.scalars().all()


async def get_champion_skins(
    session: AsyncSession, champion_name: str
) -> tuple[str, list[str]]:
    """Fetches all skins that belong to a specific champion.

    Args:
        session: Active request-scoped database session.
        champion_name: user input of a champion's name

    Returns:
        tuple[str, list[str]] | None: A tuple containing (official_name, skin_names),
        or None if no champion matches the search string.
    """
    champion_name = re.sub(r"[\s'\-\.\/:,]", "", champion_name).lower()

    statement = (
        select(models.Champion)
        .options(selectinload(models.Champion.skins))
        .where(models.Champion.search_name == champion_name)
    )

    result = await session.execute(statement)
    champion = result.scalars().first()

    return champion.name, [skin.name for skin in champion.skins]
