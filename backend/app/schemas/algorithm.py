"""Algorithm Pydantic schemas"""

from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.category import Category
from app.schemas.difficulty import DifficultyLevel
from app.schemas.code_template import CodeTemplate


class CoreFormula(BaseModel):
    """Core formula structure"""
    name: str
    formula: str
    description: str


class ApplicationConditions(BaseModel):
    """Application conditions structure"""
    when_to_use: list[str]
    when_not_to_use: list[str]


class ProblemType(BaseModel):
    """Problem type structure"""
    type: str
    leetcode_examples: list[str]


class AlgorithmBase(BaseModel):
    """Base algorithm schema"""
    title: str = Field(..., max_length=200)
    concept_summary: str
    core_formulas: Optional[list[dict[str, Any]]] = None
    thought_process: Optional[str] = None
    application_conditions: Optional[dict[str, Any]] = None
    time_complexity: str = Field(..., max_length=50)
    space_complexity: str = Field(..., max_length=50)
    problem_types: Optional[list[dict[str, Any]]] = None
    common_mistakes: Optional[str] = None


class AlgorithmCreate(AlgorithmBase):
    """Schema for creating algorithm"""
    category_id: int
    difficulty_id: int


class AlgorithmUpdate(BaseModel):
    """Schema for updating algorithm"""
    title: Optional[str] = Field(None, max_length=200)
    category_id: Optional[int] = None
    difficulty_id: Optional[int] = None
    concept_summary: Optional[str] = None
    core_formulas: Optional[list[dict[str, Any]]] = None
    thought_process: Optional[str] = None
    application_conditions: Optional[dict[str, Any]] = None
    time_complexity: Optional[str] = Field(None, max_length=50)
    space_complexity: Optional[str] = Field(None, max_length=50)
    problem_types: Optional[list[dict[str, Any]]] = None
    common_mistakes: Optional[str] = None
    is_published: Optional[bool] = None


class Algorithm(AlgorithmBase):
    """Full algorithm schema for responses"""
    id: int
    slug: str
    category: Category
    difficulty: DifficultyLevel
    code_templates: list[CodeTemplate] = []
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AlgorithmList(BaseModel):
    """Simplified algorithm schema for lists"""
    id: int
    title: str
    slug: str
    category: Category
    difficulty: DifficultyLevel
    concept_summary: str
    time_complexity: str
    space_complexity: str
    view_count: int

    model_config = {"from_attributes": True}


class PaginatedAlgorithms(BaseModel):
    """Paginated algorithm list response"""
    items: list[AlgorithmList]
    total: int
    page: int
    size: int
    pages: int
