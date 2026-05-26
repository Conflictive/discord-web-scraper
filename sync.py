"""
sync.py
~~~~~~~~~
This script is used to update database records,
it obtains the updated information from skin_manager.fetcher
and then writes it to the database using database.crud

Dependencies:
    - fetcher.py: To get updated data from the API
    - crud.py: For database operations
    - models.py: To target the destination tables
    - scraper.py: To get sale data from mobalytics
"""

import skins_manager.fetcher as fetcher
import database.crud as crud
import database.models as models
import asyncio
import skins_manager.scraper as scraper


async def update_champions():
    """
    Gets champion data from API and writes it to the database
    """
    champ_data = await fetcher.get_champion_data()
    await crud.bulk_db_write(models.Champion, champ_data)
    print("champions table successfully updated.")


async def update_skins():
    """
    Gets skin data from API and writes it to the database
    """
    skin_data = await fetcher.get_skin_data()
    await crud.bulk_db_write(models.Skin, skin_data)
    print("skins table successfully updated.")


async def update_sales():
    """Gets sale data from scraper and writes it to the database"""
    sale_data = await scraper.get_skin_sales()
    await crud.bulk_db_write(models.SkinSale, sale_data)
    print("skin_sales table successfully updated.")


async def main():
    await update_champions()
    await update_skins()
    await update_sales()


if __name__ == "__main__":
    asyncio.run(main())
