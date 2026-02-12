"""Async SQLAlchemy 2.0 database session configuration"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Create async engine
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=True,  # Set to False in production
    future=True,
    pool_pre_ping=True,

    # Connection pool configuration
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,

    # Connection arguments
    connect_args={
        # asyncpg-specific timeouts
        "timeout": settings.DB_CONNECT_TIMEOUT,
        "command_timeout": settings.DB_COMMAND_TIMEOUT,

        # Server settings
        "server_settings": {
            "timezone": "Asia/Seoul",
            "search_path": settings.POSTGRES_SCHEMA,
        },

        # SSL configuration
        "ssl": settings.DB_SSL_MODE,
    },
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
