"""Pydantic schemas for champion entities.

Defines response and request data validation models for the API.
"""

from pydantic import Field

from src.schemas.base import ORMResponseModel


class ChampionResponse(ORMResponseModel):
    """Public API response model representing champion details."""

    id: int = Field(description="Unique identifier for the champion")
    name: str = Field(description="Name of the champion", example="Rammus")
