import database.crud as crud
import database.models as models


async def test_bulk_db_write(seed_champion):
    """Test that the bulk db write actually writes to the database"""

    MOCK_DATA = [
        {"id": 330001, "name": "King Rammus", "champion_id": 33},
        {"id": 330002, "name": "Chrome Rammus", "champion_id": 33},
    ]

    await crud.bulk_db_write(models.Skin, MOCK_DATA)

    skins = await crud.get_all_from_table(models.Skin)

    assert len(skins) == 2, "Write was unsuccessful"
