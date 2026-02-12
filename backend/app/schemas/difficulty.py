"""Difficulty level Pydantic schemas"""

from pydantic import BaseModel, Field
from app.models.difficulty import DifficultyEnum


class DifficultyLevel(BaseModel):
    """Difficulty level schema"""
    id: int
    name: DifficultyEnum
    color: str = Field(..., pattern="^#[0-9A-Fa-f]{6}$")

    model_config = {"from_attributes": True}
