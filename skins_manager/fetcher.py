"""
skins_manager.fetcher
~~~~~~~~~~~~~~~~~~~~~~
This module handles API calls to the LoL community API to obtain an updated
and accurate list of all existing skins + champions.

Dependencies:
    - requests: For network calls.
"""

import requests

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


def get_skin_data():
    """
    Fetches skin data from the API to use as validation for user input

    Returns:
        - list[str]: A list of all existing skins in the game
        - None: If any network or request error occurs.
    """
    # Attempt to reach the page; wrap in try/except to handle outages
    try:
        request = requests.get(SKINS_URL, timeout=10)
        request.raise_for_status()

        data = request.json()
        # Only the name is relevant
        skins = [skin.get("name") for skin in data.values()]
        return skins
    except requests.RequestException as e:
        # If the site is down or slow, log the error and return None
        # to be handled by the calling function
        print(f"Error fetching skin data: {e}")
        return None


def get_champion_data():
    """
    Fetches champion data from the API to use as validation for user input

    Returns:
        - list[str]: A list of all existing champions in the game
        - None: If any network or request error occurs.
    """
    try:
        request = requests.get(CHAMPIONS_URL, timeout=10)
        request.raise_for_status()

        data = request.json()

        # Get a clean list of champions that removes the doom bots
        # and the 'None' champion that is at position 1
        champions = [
            {"name": champ.get("name")}
            for champ in data
            if champ.get("name") != "None" and not champ["name"].startswith("Doom")
        ]

        return champions
    except requests.RequestException as e:
        # If the site is down or slow, log the error and return None
        # to be handled by the calling function
        print(f"Error fetching champion data: {e}")
        return None


get_champion_data()
