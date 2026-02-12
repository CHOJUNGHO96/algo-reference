"""Authentication Pydantic schemas"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes in seconds


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class UserInfo(BaseModel):
    """User information schema"""
    id: int
    email: str
    role: str

    model_config = {"from_attributes": True}
