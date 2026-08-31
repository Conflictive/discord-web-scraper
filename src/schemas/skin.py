"""Pydantic schemas for skin entities.

Defines response and request data validation models for the API.
"""

from pydantic import Field

from src.schemas.base import ORMResponseModel


class SkinResponse(ORMResponseModel):
    """Public API response model representing skin details."""

    id: int = Field(description="Unique identifier for the skin")
    name: str = Field(description="Name of the skin", example="King Rammus")
