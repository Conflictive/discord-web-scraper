"""
skins_manager.scraper
~~~~~~~~~~~~~~~~~~~~~~
This module handles the web scraping on Mobalytics' weekly skin sale page.
It targets the skin name, current and old prices and also the size of the discount.

Dependencies:
    BeautifulSoup4: For HTML parsing.
    httpx: For async network error handling.
    curl_cffi: For async network calls
    database.crud: For performing database operations
    database.models: To be able to target database tables
    re: For using a regex to get the sale numbers from the scraper
"""

from bs4 import BeautifulSoup
import httpx
import database.crud as crud
import database.models as models
import re
from curl_cffi.requests import AsyncSession

# URL to the mobalytics weekly skin sale page
URL = "https://mobalytics.gg/lol/guides/weekly-skin-sale"


def clean_name(name):
    """Removes colons, hyphens, spaces, and forces lowercase for uniform matching."""
    # 1. Force lowercase
    name = name.lower()
    # 2. Strip out colons, hyphens, apostrophes, etc.
    name = re.sub(r"[:'\-\.]", "", name)
    # 3. Strip all spaces entirely so "project yasuo" matches "projectyasuo"
    name = "".join(name.split())
    return name


async def get_skin_sales():
    """
    Fetches and returns the current list of skin sales.

    Returns:
        - list[dict]: A list of all the skins that are currently on sale
        - None: If any network or request error occurs.
    """

    # Attempt to reach the page; wrap in try/except to handle outages
    async with AsyncSession() as client:
        try:
            page = await client.get(URL, impersonate="chrome")
            soup = BeautifulSoup(page.text, "html.parser")
            sale_data = soup.find_all("strong")
            # Remove HTML tags leaving just the sale data
            all_sale_data = [sale.get_text(strip=True) for sale in sale_data]

            # Instead of running a query for each skin name that appears just create the entire map so only one query is used
            skin_map = await crud.get_skin_name_to_id_map()

            # Transform {"PROJECT Yasuo": 33005} -> {"projectyasuo": 33005} to avoid issues with certain skins that may have characters like :
            skin_map = {clean_name(name): skin_id for name, skin_id in skin_map.items()}

            sales = []

            for sale in all_sale_data:
                # Skins are returned in the format 'Dragonwing Corki-390 RP (975 RP)-60% Off'
                # Splitting this way leaves only the relevant information
                # i.e [Dragonwing Corki, 390 RP (975 RP)]
                values = sale.rsplit("-", 2)

                skin_name = clean_name(values[0])
                prices = values[1]

                # Regex to find just the sale numbers from 390 RP (975 RP)
                price = re.findall(r"\d+", prices)

                # Dictionary that matches the columns of the skin_sales table
                sales.append(
                    {
                        "skin_id": skin_map[skin_name],
                        "sale_price": int(price[0]),
                        "original_price": int(price[1]),
                        "end_date": None,
                    }
                )

            return sales
        except httpx.RequestError as e:
            # If the site is down or slow, log the error and return None
            # to be handled by the calling function
            print(f"Error fetching skins: {e}")
            return None
