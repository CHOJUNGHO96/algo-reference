"""Difficulty level model"""

from sqlalchemy import String, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class DifficultyEnum(str, enum.Enum):
    """Difficulty level enumeration"""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class DifficultyLevel(Base):
    """Algorithm difficulty level"""

    __tablename__ = "difficulty_levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[DifficultyEnum] = mapped_column(
        SQLEnum(DifficultyEnum, native_enum=False, length=10),
        nullable=False,
        unique=True
    )
    color: Mapped[str] = mapped_column(String(7), nullable=False)  # Hex color code

    # Relationships
    algorithms: Mapped[list["Algorithm"]] = relationship(
        "Algorithm",
        back_populates="difficulty",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<DifficultyLevel(id={self.id}, name='{self.name.value}')>"
