"""Category endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.category import Category as CategoryModel
from app.schemas.category import Category

router = APIRouter()


@router.get("", response_model=list[Category])
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    """List all categories"""
    query = select(CategoryModel).order_by(CategoryModel.display_order)
    result = await db.execute(query)
    categories = result.scalars().all()
    return [Category.model_validate(cat) for cat in categories]


@router.get("/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get category by slug"""
    query = select(CategoryModel).filter(CategoryModel.slug == slug)
    result = await db.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return Category.model_validate(category)
