"""Skin API route handlers.

Provides REST endpoints for fetching and managing skins.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Skin as SkinModel
from src.database.repositories.base_repo import get_all_from_table
from src.database.session import get_db
from src.schemas.skin import SkinResponse

router = APIRouter(prefix="/skins", tags=["Skins"])


@router.get(
    "/",
    response_model=list[SkinResponse],
    status_code=status.HTTP_200_OK,
    summary="List all skins",
)
async def list_skins(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all skins in the database.

    Args:
        db: Injected database session

    Returns:
        A list of SkinResponse objects containing skin details.
    """
    return await get_all_from_table(db, SkinModel)
