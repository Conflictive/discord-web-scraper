import src.database.repositories.base_repo as base_repo
from src.database.models import Skin


async def test_bulk_db_write(seed_champion):
    """Test that the bulk db write actually writes to the database"""
    MOCK_DATA = [
        Skin(id=330001, name="King Rammus", search_name="kingrammus", champion_id=33),
        Skin(
            id=330002, name="Chrome Rammus", search_name="chromerammus", champion_id=33
        ),
    ]

    await base_repo.bulk_db_write(Skin, MOCK_DATA)

    skins = await base_repo.get_all_from_table(Skin)

    assert len(skins) == 2, "Write was unsuccessful"
