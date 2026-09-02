"""Champion API route handlers.

Provides REST endpoints for fetching and managing champions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Champion as ChampionModel
from src.database.repositories.base_repo import get_all_from_table
from src.database.repositories.skin_repo import get_champion_skins
from src.database.session import get_db
from src.schemas.champion import ChampionResponse

router = APIRouter(prefix="/champions", tags=["champions"])


@router.get(
    "/",
    response_model=list[ChampionResponse],
    status_code=status.HTTP_200_OK,
    summary="List all skins",
)
async def list_champions(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all champions in the database.

    Args:
        db: Injected database session

    Returns:
        A list of ChampionResponse objects containing skin details.
    """
    return await get_all_from_table(db, ChampionModel)


@router.get(
    "/{champion_name}/skins",
    response_model=tuple[str, list[str]],
    status_code=status.HTTP_200_OK,
    summary="List all of a champions skins",
)
async def list_champion_skins(champion_name: str, db: AsyncSession = Depends(get_db)):
    """Retrieves a list of a given champions skins.

    Args:
        champion_name (str): An existing champions name, must be a valid name
        db (AsyncSession, optional): Injected database session

    Returns:
        result(tuple[str, list[str]]): Final result which contains both the name
        of the champion and a list of their skins
    """
    result = await get_champion_skins(db, champion_name)

    if not result:
        raise HTTPException(
            status=status.HTTP_404_NOT_FOUND,
            detail=f"Champion with name '{champion_name}' was not found",
        )

    return result
