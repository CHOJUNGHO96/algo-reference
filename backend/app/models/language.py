"""Programming language model"""

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProgrammingLanguage(Base):
    """Programming language for code templates"""

    __tablename__ = "programming_languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    extension: Mapped[str] = mapped_column(String(10), nullable=False)  # e.g., ".py", ".js"
    prism_key: Mapped[str] = mapped_column(String(50), nullable=False)  # For Prism.js syntax highlighting

    # Relationships
    code_templates: Mapped[list["CodeTemplate"]] = relationship(
        "CodeTemplate",
        back_populates="language",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ProgrammingLanguage(id={self.id}, name='{self.name}', slug='{self.slug}')>"
