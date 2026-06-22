"""Handles the web scraping on Mobalytics' weekly skin sale page.

The scraper targets specific DOM elements, bold text in this case
to extract skin names, active sale prices, original retail prices,
and percentage discounts.
"""

import re
from typing import Any

import httpx
from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

import database.crud_skins as crud

# URL to the mobalytics weekly skin sale page
URL = "https://mobalytics.gg/lol/guides/weekly-skin-sale"


def clean_name(name: str) -> str:
    """Removes colons, hyphens, spaces, and forces lowercase for uniform matching.

    Args:
        name: Champion name or string obtained from the HTML.

    Returns:
        A clean string with all special characters, whitespace and uppercase removed
    """
    name = name.lower()
    name = re.sub(r"[:'\-\.]", "", name)
    return "".join(name.split())


async def get_skin_sales() -> list[dict[str, Any] | None]:
    """Fetches and processes the current list of skin sales.

    Uses a browser impersonating HTTP client to scrape DOM elements from the site,
    the sale details are extracted using a regex and then mapped according to
    the fields of the database

    Returns:
        A list of dictionaries matching the schema requirements of the skin sales
        database destination table, or None if a network connectivity exception occurs.
    """
    # Attempt to reach the page; wrap in try/except to handle outages
    async with AsyncSession() as client:
        try:
            page = await client.get(URL, impersonate="chrome")
            soup = BeautifulSoup(page.text, "html.parser")
            sale_data = soup.find_all("strong")
            # Remove HTML tags leaving just the sale data
            all_sale_data = [sale.get_text(strip=True) for sale in sale_data]

            # Instead of running a query for each skin name that appears
            # just create the entire map so only one query is used
            skin_map = await crud.get_skin_name_to_id_map()

            # Transform {"PROJECT Yasuo": 33005} -> {"projectyasuo": 33005}
            # to avoid issues with certain skins that may have special characters
            skin_map = {clean_name(name): skin_id for name, skin_id in skin_map.items()}

            sales = []
            for sale in all_sale_data:
                # Skins are returned in the format 'Dragonwing Corki-390 RP (975 RP)-60% Off'
                # Splitting this way leaves only the relevant information
                # i.e [Dragonwing Corki, 390 RP (975 RP)]
                values = sale.split("-", 3)

                skin_name = clean_name(values[0])

                prices = values[1] + " " + values[2]

                # Regex to find just the sale numbers from 390 RP (975 RP)
                price = re.findall(r"\d+", prices)
                print(price)
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
