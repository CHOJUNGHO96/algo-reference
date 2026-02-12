"""Algorithm endpoints - Public and Admin"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc
from sqlalchemy.orm import selectinload
import re

from app.core.database import get_db
from app.models.algorithm import Algorithm as AlgorithmModel
from app.models.category import Category as CategoryModel
from app.models.difficulty import DifficultyLevel as DifficultyModel
from app.models.code_template import CodeTemplate as CodeTemplateModel
from app.schemas.algorithm import (
    Algorithm,
    AlgorithmList,
    AlgorithmCreate,
    AlgorithmUpdate,
    PaginatedAlgorithms,
)
from app.schemas.code_template import CodeTemplate, CodeTemplateCreate
from app.api.dependencies import get_current_user

router = APIRouter()
admin_router = APIRouter()


def slugify(text: str) -> str:
    """Convert text to URL-safe slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


@router.get("", response_model=PaginatedAlgorithms)
async def list_algorithms(
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    category_id: Optional[int] = None,
    difficulty_id: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", pattern="^(title|view_count|created_at)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    """List algorithms with filtering and pagination"""
    # Build base query
    query = select(AlgorithmModel).options(
        selectinload(AlgorithmModel.category),
        selectinload(AlgorithmModel.difficulty)
    ).filter(AlgorithmModel.is_published == True)

    # Apply filters
    if category_id:
        query = query.filter(AlgorithmModel.category_id == category_id)
    if difficulty_id:
        query = query.filter(AlgorithmModel.difficulty_id == difficulty_id)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                AlgorithmModel.title.ilike(search_term),
                AlgorithmModel.concept_summary.ilike(search_term)
            )
        )

    # Count total before pagination
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply sorting
    sort_column = getattr(AlgorithmModel, sort_by)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Apply pagination
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)

    # Execute query
    result = await db.execute(query)
    algorithms = result.scalars().all()

    # Calculate total pages
    pages = (total + size - 1) // size if total > 0 else 0

    return PaginatedAlgorithms(
        items=[AlgorithmList.model_validate(alg) for alg in algorithms],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{slug}", response_model=Algorithm)
async def get_algorithm_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get algorithm by slug"""
    query = select(AlgorithmModel).options(
        selectinload(AlgorithmModel.category),
        selectinload(AlgorithmModel.difficulty),
        selectinload(AlgorithmModel.code_templates).selectinload(CodeTemplateModel.language)
    ).filter(AlgorithmModel.slug == slug)

    result = await db.execute(query)
    algorithm = result.scalar_one_or_none()

    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )

    # Increment view count
    algorithm.view_count += 1
    await db.commit()

    return Algorithm.model_validate(algorithm)


@admin_router.post("", response_model=Algorithm, status_code=status.HTTP_201_CREATED)
async def create_algorithm(
    algorithm_in: AlgorithmCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Create new algorithm (Admin only)"""
    # Generate slug from title
    slug = slugify(algorithm_in.title)

    # Check if slug already exists
    existing = await db.execute(
        select(AlgorithmModel).filter(AlgorithmModel.slug == slug)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Algorithm with slug '{slug}' already exists"
        )

    # Verify category and difficulty exist
    category = await db.get(CategoryModel, algorithm_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {algorithm_in.category_id} not found"
        )

    difficulty = await db.get(DifficultyModel, algorithm_in.difficulty_id)
    if not difficulty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Difficulty level {algorithm_in.difficulty_id} not found"
        )

    # Create algorithm
    algorithm = AlgorithmModel(
        title=algorithm_in.title,
        slug=slug,
        category_id=algorithm_in.category_id,
        difficulty_id=algorithm_in.difficulty_id,
        concept_summary=algorithm_in.concept_summary,
        core_formulas=algorithm_in.core_formulas,
        thought_process=algorithm_in.thought_process,
        application_conditions=algorithm_in.application_conditions,
        time_complexity=algorithm_in.time_complexity,
        space_complexity=algorithm_in.space_complexity,
        problem_types=algorithm_in.problem_types,
        common_mistakes=algorithm_in.common_mistakes,
        is_published=False  # Default to unpublished
    )

    db.add(algorithm)
    await db.commit()
    await db.refresh(algorithm)

    # Load relationships
    query = select(AlgorithmModel).options(
        selectinload(AlgorithmModel.category),
        selectinload(AlgorithmModel.difficulty),
        selectinload(AlgorithmModel.code_templates)
    ).filter(AlgorithmModel.id == algorithm.id)
    result = await db.execute(query)
    algorithm = result.scalar_one()

    return Algorithm.model_validate(algorithm)


@admin_router.put("/{id}", response_model=Algorithm)
async def update_algorithm(
    id: int,
    algorithm_in: AlgorithmUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Update algorithm (Admin only)"""
    # Get existing algorithm
    algorithm = await db.get(AlgorithmModel, id)
    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )

    # Update fields that are provided
    update_data = algorithm_in.model_dump(exclude_unset=True)

    # Handle title update (regenerate slug)
    if "title" in update_data and update_data["title"]:
        new_slug = slugify(update_data["title"])
        if new_slug != algorithm.slug:
            # Check if new slug already exists
            existing = await db.execute(
                select(AlgorithmModel).filter(
                    AlgorithmModel.slug == new_slug,
                    AlgorithmModel.id != id
                )
            )
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Algorithm with slug '{new_slug}' already exists"
                )
            algorithm.slug = new_slug

    # Verify category if being updated
    if "category_id" in update_data and update_data["category_id"]:
        category = await db.get(CategoryModel, update_data["category_id"])
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category {update_data['category_id']} not found"
            )

    # Verify difficulty if being updated
    if "difficulty_id" in update_data and update_data["difficulty_id"]:
        difficulty = await db.get(DifficultyModel, update_data["difficulty_id"])
        if not difficulty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Difficulty level {update_data['difficulty_id']} not found"
            )

    # Apply updates
    for field, value in update_data.items():
        if hasattr(algorithm, field):
            setattr(algorithm, field, value)

    await db.commit()
    await db.refresh(algorithm)

    # Load relationships
    query = select(AlgorithmModel).options(
        selectinload(AlgorithmModel.category),
        selectinload(AlgorithmModel.difficulty),
        selectinload(AlgorithmModel.code_templates).selectinload(CodeTemplateModel.language)
    ).filter(AlgorithmModel.id == id)
    result = await db.execute(query)
    algorithm = result.scalar_one()

    return Algorithm.model_validate(algorithm)


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_algorithm(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Delete algorithm (Admin only)"""
    algorithm = await db.get(AlgorithmModel, id)
    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )

    await db.delete(algorithm)
    await db.commit()
    return None


@admin_router.post("/{id}/templates", response_model=CodeTemplate, status_code=status.HTTP_201_CREATED)
async def add_code_template(
    id: int,
    template_in: CodeTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Add code template to algorithm (Admin only)"""
    # Verify algorithm exists
    algorithm = await db.get(AlgorithmModel, id)
    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )

    # Create code template
    template = CodeTemplateModel(
        algorithm_id=id,
        language_id=template_in.language_id,
        code=template_in.code,
        explanation=template_in.explanation
    )

    db.add(template)
    try:
        await db.commit()
        await db.refresh(template)
    except Exception as e:
        await db.rollback()
        # Check if it's a duplicate language for this algorithm
        if "unique" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code template for this language already exists for this algorithm"
            )
        raise

    # Load language relationship
    from app.models.language import ProgrammingLanguage
    query = select(CodeTemplateModel).options(
        selectinload(CodeTemplateModel.language)
    ).filter(CodeTemplateModel.id == template.id)
    result = await db.execute(query)
    template = result.scalar_one()

    return CodeTemplate.model_validate(template)
