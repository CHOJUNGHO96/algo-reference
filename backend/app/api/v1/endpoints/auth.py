"""Authentication endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_refresh_token
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserInfo
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Admin login"""
    # Query user by email
    result = await db.execute(
        select(User).filter(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=900  # 15 minutes
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token"""
    # Verify refresh token
    payload = verify_refresh_token(refresh_request.refresh_token)

    # Extract user ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Verify user still exists
    user = await db.get(User, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Create new tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=900
    )


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user info"""
    return UserInfo(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role.value
    )
