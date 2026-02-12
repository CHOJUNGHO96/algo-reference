"""
Integration tests for Authentication API endpoints.

Tests the following endpoints:
- POST /api/v1/auth/login - User login
- POST /api/v1/auth/refresh - Refresh access token
- GET /api/v1/auth/me - Get current user info
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    """Test successful login with valid credentials."""
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@user.com",
        "password": "testpass123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_invalid_email(client: AsyncClient):
    """Test login with non-existent email."""
    response = await client.post("/api/v1/auth/login", json={
        "email": "nonexistent@user.com",
        "password": "testpass123"
    })

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, test_user):
    """Test login with incorrect password."""
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@user.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_missing_fields(client: AsyncClient):
    """Test login with missing required fields."""
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@user.com"
        # Missing password
    })

    assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_invalid_email_format(client: AsyncClient):
    """Test login with invalid email format."""
    response = await client.post("/api/v1/auth/login", json={
        "email": "not-an-email",
        "password": "testpass123"
    })

    assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, test_user):
    """Test successful token refresh."""
    # First login to get refresh token
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "test@user.com",
        "password": "testpass123"
    })
    refresh_token = login_response.json()["refresh_token"]

    # Use refresh token to get new access token
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    """Test refresh with invalid token."""
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": "invalid-token"
    })

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user_success(client: AsyncClient, user_token: str):
    """Test getting current user info with valid token."""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@user.com"
    assert data["role"] == "user"
    assert "id" in data
    assert "password_hash" not in data  # Sensitive field should not be exposed


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient):
    """Test getting current user without authentication."""
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient):
    """Test getting current user with invalid token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = await client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_admin_login(client: AsyncClient, test_admin):
    """Test admin user can login and has admin role."""
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "adminpass123"
    })

    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Verify admin role
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = await client.get("/api/v1/auth/me", headers=headers)

    assert me_response.status_code == 200
    data = me_response.json()
    assert data["role"] == "admin"
