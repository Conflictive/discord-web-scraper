"""
skins_manager.scraper
~~~~~~~~~~~~~~~~~~~~~~
This module handles the web scraping on Mobalytics' weekly skin sale page.
It targets the skin name, current and old prices and also the size of the discount.

Dependencies:
    BeautifulSoup4: For HTML parsing.
    httpx: For async network error handling.
    curl_cffi: For async network calls
"""

from bs4 import BeautifulSoup
import httpx
from curl_cffi.requests import AsyncSession

# URL to the mobalytics weekly skin sale page
URL = "https://mobalytics.gg/lol/guides/weekly-skin-sale"


async def get_skin_sales():
    """
    Fetches and returns the current list of skin sales.

    Returns:
        - list[str]: A list of all the skins that are currently on sale
        - None: If any network or request error occurs.
    """

    # Attempt to reach the page; wrap in try/except to handle outages
    async with AsyncSession() as client:
        try:
            page = await client.get(URL, impersonate="chrome")
            soup = BeautifulSoup(page.text, "html.parser")
            skin_data = soup.find_all("strong")

            return [skin.text.strip() for skin in skin_data if skin.text.strip()]
        except httpx.RequestError as e:
            # If the site is down or slow, log the error and return None
            # to be handled by the calling function
            print(f"Error fetching skins: {e}")
            return None
