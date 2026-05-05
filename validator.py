import requests

SKINS_URL = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json"


def get_skin_data():
    """Fetch skin + champion data from the API to use as validation for user input"""
    try:
        request = requests.get(SKINS_URL, timeout=10)
        data = request.json()
        skins = [skin.get("name") for skin in data.values()]
        return skins
    except Exception as e:
        return [f"Error fetching skin data: {e}"]
