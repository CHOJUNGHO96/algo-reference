"""Programming language Pydantic schemas"""

from pydantic import BaseModel, Field


class ProgrammingLanguage(BaseModel):
    """Programming language schema"""
    id: int
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    extension: str = Field(..., max_length=10)
    prism_key: str = Field(..., max_length=50)

    model_config = {"from_attributes": True}
