"""Champion API route handlers.

Provides REST endpoints for fetching and managing champions.
"""

from fastapi import APIRouter, status

from src.database.models import Champion as ChampionModel
from src.database.repositories.base_repo import get_all_from_table
from src.schemas.champion import ChampionResponse

router = APIRouter(prefix="/champions", tags=["champions"])


@router.get(
    "/",
    response_model=list[ChampionResponse],
    status_code=status.HTTP_200_OK,
    summary="List all skins",
)
async def list_champions():
    """Retrieves a list of all champions in the database.

    Returns:
        A list of ChampionResponse objects containing skin details.
    """
    return await get_all_from_table(ChampionModel)
