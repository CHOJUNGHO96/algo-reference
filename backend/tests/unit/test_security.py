"""
Unit tests for security utilities.

Tests password hashing, JWT token generation/validation, and authentication helpers.
"""

import pytest
from datetime import timedelta
from jose import jwt

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.core.config import get_settings

settings = get_settings()


@pytest.mark.unit
def test_password_hashing():
    """Test password hashing creates different hashes for same password."""
    password = "testpassword123"

    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Hashes should be different (due to salt)
    assert hash1 != hash2
    # Both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)


@pytest.mark.unit
def test_verify_password_success():
    """Test password verification with correct password."""
    password = "mypassword"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True


@pytest.mark.unit
def test_verify_password_failure():
    """Test password verification with incorrect password."""
    password = "mypassword"
    hashed = get_password_hash(password)

    assert verify_password("wrongpassword", hashed) is False


@pytest.mark.unit
def test_create_access_token():
    """Test access token creation and decoding."""
    data = {"sub": "user@example.com", "role": "admin"}
    token = create_access_token(data)

    # Decode token
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    assert decoded["sub"] == "user@example.com"
    assert decoded["role"] == "admin"
    assert "exp" in decoded


@pytest.mark.unit
def test_create_access_token_custom_expiry():
    """Test access token with custom expiration time."""
    data = {"sub": "user@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta=expires_delta)

    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    assert decoded["sub"] == "user@example.com"
    assert "exp" in decoded


@pytest.mark.unit
def test_create_refresh_token():
    """Test refresh token creation and decoding."""
    data = {"sub": "user@example.com"}
    token = create_refresh_token(data)

    decoded = jwt.decode(
        token,
        settings.REFRESH_SECRET_KEY,
        algorithms=["HS256"]
    )

    assert decoded["sub"] == "user@example.com"
    assert "exp" in decoded


@pytest.mark.unit
def test_tokens_are_different():
    """Test that access and refresh tokens are different."""
    data = {"sub": "user@example.com"}

    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    assert access_token != refresh_token
