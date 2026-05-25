from skins_manager.scraper import get_skin_sales
import warnings

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*set_event_loop_policy.*"
)


async def test_get_skin_sales_returns_valid_data():
    """Test that the scraper connects, reads, and returns a list of strings."""

    result = await get_skin_sales()

    print("\n--- MOBALYTICS SCRAPER OUTPUT ---")
    print(result)
    print(f"Total skins found: {len(result)}")
    print("---------------------------------")

    assert (
        len(result) > 0
    ), "Scraper returned None, network or exception block triggered."

    assert isinstance(result, list), f"Expected a list, got {type(result)} instead."

    # If there are active sales, verify the list contains string names
    if len(result) > 0:
        assert isinstance(result[0], str), "Expected skin names to be strings."
        print(f"\nScraper working. Parsed sample data: {result[:3]}")
