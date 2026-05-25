import skins_manager.fetcher as fetcher


async def test_get_champion_data_returns_valid_data():
    """Test that fetcher function can connect, read and return champion data from API"""

    result = await fetcher.get_champion_data()

    assert (
        len(result) > 0
    ), "Function returned nothing, network or exception block triggered"

    assert isinstance(result, list), f"Expected a list, got {type(result)} instead."

    if len(result) > 0:
        assert isinstance(
            result[0], dict
        ), "Expected skin names to be in dictionary format."
        print(f"\nChampion fetcher working. Parsed sample data: {result[:3]}")


async def test_get_skin_data_returns_valid_data():
    """Test that fetcher function can connect, read and return skin data from API"""

    result = await fetcher.get_skin_data()

    assert (
        len(result) > 0
    ), "Function returned nothing, network or exception block triggered"

    assert isinstance(result, list), f"Expected a list, got {type(result)} instead."

    if len(result) > 0:
        assert isinstance(
            result[0], dict
        ), "Expected skin names to be in dictionary format."
        print(f"\nSkin fetcher working. Parsed sample data: {result[:3]}")
