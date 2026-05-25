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
"""

import skins_manager.fetcher as fetcher
import database.crud as crud
import database.models as models
import asyncio


async def update_champions():
    """
    Gets champion data from API and writes it to the database
    """
    champ_data = fetcher.get_champion_data()
    await crud.bulk_db_write(models.Champion, champ_data)
    print("champions table successfully updated.")


async def update_skins():
    """
    Gets skin data from API and writes it to the database
    """
    skin_data = fetcher.get_skin_data()
    await crud.bulk_db_write(models.Skin, skin_data)
    print("skins table successfully updated.")


async def main():
    await update_champions()
    await update_skins()


if __name__ == "__main__":
    asyncio.run(main())
