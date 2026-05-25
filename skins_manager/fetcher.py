"""
skins_manager.fetcher
~~~~~~~~~~~~~~~~~~~~~~
This module handles API calls to the LoL community API to obtain an updated
and accurate list of all existing skins + champions.

Dependencies:
    - httpx: For network calls.
"""

import httpx

# URL to the LoL community API, specifically for all skins
SKINS_URL = (
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/"
    "global/default/v1/skins.json"
)

# URL for all champions
CHAMPIONS_URL = (
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/"
    "global/default/v1/champion-summary.json"
)


async def get_skin_data():
    """
    Fetches skin data from the API to use as validation for user input

    Returns:
        - list[dict]: A list of dictionaries for all existing skins in the game, Contains:
            - id(int): Identifier for each skin
            - name(str): Name of the skin
            - champion_id(int): The ID of the champion that the skin belongs to

        - None: If any network or request error occurs.
    """
    # Attempt to reach the page; wrap in try/except to handle outages
    async with httpx.AsyncClient as client:
        try:
            request = client.get(SKINS_URL, timeout=10)
            request.raise_for_status()

            data = request.json()
            clean_skins = []

            for skin_id, skin_info in data.items():
                # The base skin is always just the champion itself
                # We already have a database of all champions so this is redundant
                if skin_info.get("isBase"):
                    continue

                skin_id = int(skin_id)

                # Base skin ids in the API are created by multiplying the champion id by 1000.
                # For example Jinx's id is 222 so her base skin is 222000.
                # So each actual skin is this base skin id + 1 for each skin.
                # Dividing by 1000 gives you the champions id
                champion_id = skin_id // 1000

                # The data needs to be cleaned so that it matches the columns of the database
                clean_skins.append(
                    {
                        "id": skin_id,
                        "name": skin_info.get("name"),
                        "champion_id": champion_id,
                    }
                )

            return clean_skins
        except httpx.RequestError as e:
            # If the site is down or slow, log the error and return None
            # to be handled by the calling function
            print(f"Error fetching skin data: {e}")
            return None


async def get_champion_data():
    """
    Fetches champion data from the API to use as validation for user input. Removes irrelevant data (doom bots)

    Returns:
        - list[dict]: A list of dictionaries for all existing champions in the game. Contains:
            - id(int): Identifier for each champion
            - name(str): Name of the champion

        - None: If any network or request error occurs.
    """
    async with httpx.AsyncClient as client:
        try:
            request = client.get(CHAMPIONS_URL, timeout=10)
            request.raise_for_status()

            data = request.json()

            # Get a clean list of champions that removes the doom bots
            # and the 'None' champion that is at position 1
            champions = [
                {"id": champ.get("id"), "name": champ.get("name")}
                for champ in data
                if champ.get("name") != "None" and not champ["name"].startswith("Doom")
            ]

            return champions
        except httpx.RequestError as e:
            # If the site is down or slow, log the error and return None
            # to be handled by the calling function
            print(f"Error fetching champion data: {e}")
            return None
