"""Category Pydantic schemas"""

from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: Optional[str] = None
    display_order: int = Field(default=0)
    parent_id: Optional[int] = None
    color: str = Field(default="#0969da", pattern="^#[0-9A-Fa-f]{6}$")


class Category(CategoryBase):
    """Full category schema for responses"""
    id: int

    model_config = {"from_attributes": True}


class CategoryList(BaseModel):
    """Simplified category schema for lists"""
    id: int
    name: str
    slug: str
    color: str

    model_config = {"from_attributes": True}
