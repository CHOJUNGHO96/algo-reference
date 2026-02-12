"""Code template model for algorithm implementations"""

from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CodeTemplate(Base):
    """Code implementation template for algorithms"""

    __tablename__ = "code_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign keys
    algorithm_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("algorithms.id", ondelete="CASCADE"),
        nullable=False
    )
    language_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("programming_languages.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Content
    code: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    algorithm: Mapped["Algorithm"] = relationship("Algorithm", back_populates="code_templates")
    language: Mapped["ProgrammingLanguage"] = relationship("ProgrammingLanguage", back_populates="code_templates")

    # Ensure one template per language per algorithm
    __table_args__ = (
        UniqueConstraint("algorithm_id", "language_id", name="uq_algorithm_language"),
    )

    def __repr__(self) -> str:
        return f"<CodeTemplate(id={self.id}, algorithm_id={self.algorithm_id}, language_id={self.language_id})>"
