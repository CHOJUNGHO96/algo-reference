"""Create admin user for development/testing"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole


async def create_admin_user():
    """Create default admin user"""
    # Create async engine
    engine = create_async_engine(
        str(settings.DATABASE_URL),
        echo=True,
    )

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Check if admin already exists
        from sqlalchemy import select
        result = await session.execute(
            select(User).filter(User.email == settings.FIRST_ADMIN_EMAIL)
        )
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print(f"✅ Admin user already exists: {settings.FIRST_ADMIN_EMAIL}")
            return

        # Create admin user
        admin = User(
            email=settings.FIRST_ADMIN_EMAIL,
            password_hash=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
            role=UserRole.ADMIN
        )

        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        print(f"✅ Admin user created successfully!")
        print(f"   Email: {admin.email}")
        print(f"   Password: {settings.FIRST_ADMIN_PASSWORD}")
        print(f"   Role: {admin.role.value}")
        print(f"\n⚠️  IMPORTANT: Change the password in production!")

    await engine.dispose()


if __name__ == "__main__":
    print("Creating admin user...")
    asyncio.run(create_admin_user())
