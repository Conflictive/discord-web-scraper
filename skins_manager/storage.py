import json
import skins_manager.fetcher as fetcher


def store_skin_data():
    """Fetches skin information and then stores it into a json file to be used for validation"""
    skins = fetcher.get_skin_data()

    skins_json = json.dumps(skins, indent=4)

    with open("skins.json", "w", encoding="utf-8") as f:
        f.write(skins_json)


if __name__ == "__main__":
    store_skin_data()
