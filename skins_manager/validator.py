import skins_manager.storage as storage
import json
from pathlib import Path

# Get to the root
BASE_DIR = Path(__file__).parent.parent
# Target the data file
DATA_DIR = BASE_DIR / "data"
# Target the skins.json file
FILE_PATH = DATA_DIR / "skins.json"


def check_skin():
    with open("data.json", "r") as file:
        data = json.load(file)
