"""User model for admin authentication"""

from sqlalchemy import String, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    EDITOR = "editor"


class User(Base):
    """Admin user for CMS authentication"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, native_enum=False, length=20),
        nullable=False,
        default=UserRole.EDITOR
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"
