"""
skins_manager.storage
~~~~~~~~~~~~~~~~~~~~~~
This module writes the skin data obtained by the fetcher module into
a JSON file using store_skin_data().

It also opens that same JSON file to be used by the validator module using open_skin_file().

Dependencies:
    - json: For reading and writing to json files
    - Path: For constructing a path variable for the file
    - fetcher: Module to get the skin data before writing
"""

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
    """Gets skin information from the fetcher module and then stores it into a json file to be used for validation"""
    skins = fetcher.get_skin_data()

    skins_json = json.dumps(skins, indent=4)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(skins_json)


def open_skin_file():
    """
    Opens the json containing all valid skins and returning them as a dictionary

    Returns:
        - dict: The parsed JSON object as a Python dictionary.
        - None: If the file is missing or contains invalid JSON.
    """
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            # json.load() converts the file content into a Python dict
            data = json.load(file)
            return data

    except (FileNotFoundError, json.JSONDecodeError) as e:
        # Handle cases where file doesn't exist or isn't valid JSON
        print(f"Configuration error: {e}")
        return None
