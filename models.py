"""Pydantic models for API validation and serialization."""

from pydantic import BaseModel, Field  # pylint: disable=import-error


# Pydantic models for API validation
class ItemCreate(BaseModel):  # pylint: disable=too-few-public-methods
    """Model for creating a new item."""

    text: str = Field(..., min_length=1, description="Text content of the item")


class ItemUpdate(BaseModel):  # pylint: disable=too-few-public-methods
    """Model for updating an existing item."""

    text: str = Field(..., min_length=1, description="Updated text content")


class Item(BaseModel):  # pylint: disable=too-few-public-methods
    """Model for item responses."""

    id: int
    text: str

    model_config = {"from_attributes": True}
