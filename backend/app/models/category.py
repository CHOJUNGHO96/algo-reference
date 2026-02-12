"""Category model for algorithm categorization"""

from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Category(Base):
    """Algorithm category with hierarchical support"""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    color: Mapped[str] = mapped_column(String(7), default="#0969da")  # Hex color code

    # Self-referential relationship for hierarchical categories
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relationships
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    algorithms: Mapped[list["Algorithm"]] = relationship(
        "Algorithm",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}', slug='{self.slug}')>"
