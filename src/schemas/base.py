"""Pydantic schema for all ORM schemas to use.

Converts db objects to camelCase JSON.
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ORMResponseModel(BaseModel):
    """Base response model for converting db objects to camelCase JSON."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )
