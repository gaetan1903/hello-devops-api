from pydantic import BaseModel, Field


# Pydantic models for API validation
class ItemCreate(BaseModel):
    text: str = Field(..., min_length=1, description="Text content of the item")


class ItemUpdate(BaseModel):
    text: str = Field(..., min_length=1, description="Updated text content")


class Item(BaseModel):
    id: int
    text: str
    
    model_config = {"from_attributes": True}
