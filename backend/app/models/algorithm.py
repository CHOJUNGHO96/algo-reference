"""Algorithm model with 8-point content structure"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, TIMESTAMP, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR

from app.core.database import Base


class Algorithm(Base):
    """Algorithm with comprehensive learning content"""

    __tablename__ = "algorithms"

    # Primary fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)

    # Foreign keys
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False
    )
    difficulty_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("difficulty_levels.id", ondelete="RESTRICT"),
        nullable=False
    )

    # 8-Point Content Structure
    concept_summary: Mapped[str] = mapped_column(Text, nullable=False)
    core_formulas: Mapped[Optional[list[dict]]] = mapped_column(JSONB, nullable=True)
    thought_process: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    application_conditions: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    time_complexity: Mapped[str] = mapped_column(String(50), nullable=False)
    space_complexity: Mapped[str] = mapped_column(String(50), nullable=False)
    problem_types: Mapped[Optional[list[dict]]] = mapped_column(JSONB, nullable=True)
    common_mistakes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Publishing and analytics
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    # Full-text search (PostgreSQL specific)
    search_vector: Mapped[Optional[str]] = mapped_column(TSVECTOR, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    category: Mapped["Category"] = relationship("Category", back_populates="algorithms")
    difficulty: Mapped["DifficultyLevel"] = relationship("DifficultyLevel", back_populates="algorithms")
    code_templates: Mapped[list["CodeTemplate"]] = relationship(
        "CodeTemplate",
        back_populates="algorithm",
        cascade="all, delete-orphan"
    )

    # Indexes for performance
    __table_args__ = (
        Index("ix_algorithms_category_difficulty", "category_id", "difficulty_id"),
        Index("ix_algorithms_published_created", "is_published", "created_at"),
        Index("ix_algorithms_search_vector", "search_vector", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<Algorithm(id={self.id}, title='{self.title}', slug='{self.slug}')>"
