"""Programming language endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.language import ProgrammingLanguage

router = APIRouter()


@router.get("", response_model=list[ProgrammingLanguage])
async def list_languages(
    db: AsyncSession = Depends(get_db),
):
    """List all programming languages (stub)"""
    # TODO: Implement actual database query
    return []
