from bs4 import BeautifulSoup
import requests

URL = "https://mobalytics.gg/lol/guides/weekly-skin-sale"


def get_skin_sales():
    """Fetches and returns the current list of skin sales."""
    try:
        page = requests.get(URL, timeout=10)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, "html.parser")
        skins = soup.find_all("strong")
        return [skin.text.strip() for skin in skins if skin.text.strip()]
    except Exception as e:
        return [f"Error fetching skins: {e}"]
