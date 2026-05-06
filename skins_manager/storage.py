import json
from pathlib import Path
import skins_manager.fetcher as fetcher

# Get to the root
BASE_DIR = Path(__file__).parent.parent
# Target the data file
DATA_DIR = BASE_DIR / "data"
# Target the skins.json file
FILE_PATH = DATA_DIR / "skins.json"

# Make data file if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


def store_skin_data():
    """Fetches skin information and then stores it into a json file to be used for validation"""
    skins = fetcher.get_skin_data()

    skins_json = json.dumps(skins, indent=4)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(skins_json)


def open_skin_file():
    "Opens the json containing all valid skins and returning them as a list"
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
