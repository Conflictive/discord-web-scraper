"""Skin API route handlers.

Provides REST endpoints for fetching and managing skins.
"""

from fastapi import APIRouter, status

from src.database.models import Skin as SkinModel
from src.database.repositories.base_repo import get_all_from_table
from src.schemas.skin import SkinResponse

router = APIRouter(prefix="/skins", tags=["Skins"])


@router.get(
    "/",
    response_model=list[SkinResponse],
    status_code=status.HTTP_200_OK,
    summary="List all skins",
)
async def list_skins():
    """Retrieves a list of all skins in the database.

    Returns:
        A list of SkinResponse objects containing skin details.
    """
    return await get_all_from_table(SkinModel)
