"""crud_skins.py
~~~~~~~~~~~~~~
Module containing CRUD operations that are relevant to skins
"""

import re

from sqlalchemy import select
from sqlalchemy.orm import selectinload

import src.database.models as models
from src.database.session import AsyncSessionLocal


async def get_skin_name_to_id_map():
    """Fetches all skins once and returns a dict mapping {name: id}.

    Returns:
        dict: in the format {name: id} ({Rammus: 33})
    """
    async with AsyncSessionLocal() as session:
        statement = select(models.Skin.name, models.Skin.id)
        result = await session.execute(statement)
        return dict(result.all())


async def get_active_sales_with_skins():
    """Fetches all sales and loads their connected skin models.

    Returns:
        list: containing SQLAlchemy model objects
    """
    async with AsyncSessionLocal() as session:
        statement = select(models.SkinSale).options(selectinload(models.SkinSale.skin))

        result = await session.execute(statement)
        return result.scalars().all()


async def get_champion_skins(champion_name):
    """Fetches all skins that belong to a specific champion.

    Args:
        champion_name (str): user input of a champion's name

    Returns:
        list[str]: containing the champions skin names
    """
    champion_name = re.sub(r"[\s'\-\.\/:,]", "", champion_name).lower()

    async with AsyncSessionLocal() as session:
        statement = (
            select(models.Champion)
            .options(selectinload(models.Champion.skins))
            .where(models.Champion.search_name == champion_name)
        )

        result = await session.execute(statement)
        champion = result.scalars().first()

        return champion.name, [skin.name for skin in champion.skins]
