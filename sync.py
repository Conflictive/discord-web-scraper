"""
sync.py
~~~~~~~~~
This script is used to update database records,
it obtains the updated information from skin_manager.fetcher
and then writes it to the database using database.crud

Dependencies:
    - fetcher.py: To get updated data from the API
    - crud.py: For database operations
"""

import skins_manager.fetcher as fetcher
import database.crud as crud


def update_champions():
    """
    Gets champion data from API and writes it to the database
    """
    champ_data = fetcher.get_champion_data()
    crud.bulk_db_write(champ_data)
    print("Database successfully updated.")


if __name__ == "__main__":
    update_champions()
