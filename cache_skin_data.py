import json
import validator


def store_file():
    """Fetches skin information and then stores it into a json file to be used for validation"""
    skins = validator.get_skin_data()

    skins_json = json.dumps(skins, indent=4)

    with open("skins.json", "w") as f:
        f.write(skins_json)


if __name__ == "__main__":
    store_file()
