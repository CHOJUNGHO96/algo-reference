"""Pydantic schemas for request/response validation"""

from app.schemas.category import Category, CategoryList
from app.schemas.difficulty import DifficultyLevel
from app.schemas.language import ProgrammingLanguage
from app.schemas.code_template import CodeTemplate, CodeTemplateCreate
from app.schemas.algorithm import (
    Algorithm,
    AlgorithmList,
    AlgorithmCreate,
    AlgorithmUpdate,
    PaginatedAlgorithms,
)
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserInfo,
)

__all__ = [
    "Category",
    "CategoryList",
    "DifficultyLevel",
    "ProgrammingLanguage",
    "CodeTemplate",
    "CodeTemplateCreate",
    "Algorithm",
    "AlgorithmList",
    "AlgorithmCreate",
    "AlgorithmUpdate",
    "PaginatedAlgorithms",
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "UserInfo",
]
