"""Code template Pydantic schemas"""

from typing import Optional
from pydantic import BaseModel

from app.schemas.language import ProgrammingLanguage


class CodeTemplateBase(BaseModel):
    """Base code template schema"""
    code: str
    explanation: Optional[str] = None


class CodeTemplateCreate(CodeTemplateBase):
    """Schema for creating code template"""
    language_id: int


class CodeTemplate(CodeTemplateBase):
    """Full code template schema for responses"""
    id: int
    algorithm_id: int
    language: ProgrammingLanguage

    model_config = {"from_attributes": True}
