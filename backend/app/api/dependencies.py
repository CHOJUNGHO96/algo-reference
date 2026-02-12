"""FastAPI dependencies for authentication and authorization"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_access_token
from app.models.user import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Validate JWT token and return current user
    Used as dependency for protected endpoints
    """
    token = credentials.credentials

    # Verify and decode token
    payload = verify_access_token(token)

    # Extract user ID from token
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Query user from database (stub - will be implemented in Phase 2)
    # TODO: Implement actual user query
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verify that current user has admin role
    Used for admin-only endpoints
    """
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    return current_user
