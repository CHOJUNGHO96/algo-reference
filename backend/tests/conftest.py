"""
Pytest configuration and fixtures for Algorithm Reference Platform tests.

This module provides reusable test fixtures and configuration for:
- Database session management with automatic rollback
- Test client for API testing
- Authentication fixtures for protected endpoints
- Test data factories for models
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings
from app.core.security import get_password_hash

# Test database URL (separate from development database)
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/algoref_test"

# Override settings for testing
settings.DATABASE_URL = TEST_DATABASE_URL
settings.SECRET_KEY = "test-secret-key-change-in-production"

# Create test engine with NullPool (new connection per request)
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,  # Set to True for SQL query debugging
)

# Create async session maker
test_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create event loop for async tests.

    Scope: session - One loop for all tests
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create clean database session for each test.

    - Drops all tables before test
    - Creates fresh schema
    - Yields session for test usage
    - Rolls back any changes after test

    Scope: function - New session per test for isolation
    """
    # Drop and recreate all tables for clean state
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with test_session_maker() as session:
        yield session
        # Rollback any uncommitted changes
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test client with database override.

    - Overrides app's database dependency with test session
    - Provides AsyncClient for making HTTP requests
    - Clears dependency overrides after test

    Scope: function - New client per test

    Usage:
        async def test_example(client: AsyncClient):
            response = await client.get("/api/v1/algorithms")
            assert response.status_code == 200
    """
    async def override_get_db():
        yield db_session

    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client

    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_category(db_session: AsyncSession):
    """
    Create test category fixture.

    Returns a Category model instance for testing.
    """
    from app.models.category import Category

    category = Category(
        name="Two Pointer",
        slug="two-pointer",
        description="Two pointer technique algorithms",
        color="#0969da"
    )
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    return category


@pytest_asyncio.fixture
async def test_difficulty(db_session: AsyncSession):
    """
    Create test difficulty level fixture.

    Returns a DifficultyLevel model instance for testing.
    """
    from app.models.difficulty import DifficultyLevel

    difficulty = DifficultyLevel(
        name="Medium",
        color="#d29922"
    )
    db_session.add(difficulty)
    await db_session.commit()
    await db_session.refresh(difficulty)

    return difficulty


@pytest_asyncio.fixture
async def test_language(db_session: AsyncSession):
    """
    Create test programming language fixture.

    Returns a Language model instance for testing.
    """
    from app.models.language import Language

    language = Language(
        name="Python",
        slug="python",
        monaco_language="python"
    )
    db_session.add(language)
    await db_session.commit()
    await db_session.refresh(language)

    return language


@pytest_asyncio.fixture
async def test_algorithm(db_session: AsyncSession, test_category, test_difficulty):
    """
    Create test algorithm fixture.

    Returns a fully populated Algorithm model instance for testing.
    Includes category and difficulty relationships.
    """
    from app.models.algorithm import Algorithm

    algorithm = Algorithm(
        title="Two Pointer Technique",
        slug="two-pointer-technique",
        category_id=test_category.id,
        difficulty_id=test_difficulty.id,
        concept_summary="The two pointer technique uses two indices to traverse data structures...",
        core_formulas="left = 0, right = len(arr) - 1",
        thought_process="1. Initialize two pointers\n2. Move pointers based on condition\n3. Process elements",
        application_conditions="Sorted array, palindrome checking, pair sum problems",
        time_complexity="O(n)",
        space_complexity="O(1)",
        problem_types="Pair sum, remove duplicates, palindrome validation",
        common_mistakes="Off-by-one errors, incorrect pointer movement",
        is_published=True,
        view_count=0
    )
    db_session.add(algorithm)
    await db_session.commit()
    await db_session.refresh(algorithm)

    return algorithm


@pytest_asyncio.fixture
async def test_code_template(db_session: AsyncSession, test_algorithm, test_language):
    """
    Create test code template fixture.

    Returns a CodeTemplate model instance for testing.
    """
    from app.models.code_template import CodeTemplate

    code_template = CodeTemplate(
        algorithm_id=test_algorithm.id,
        language_id=test_language.id,
        code="""def two_pointer(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []""",
        order=1
    )
    db_session.add(code_template)
    await db_session.commit()
    await db_session.refresh(code_template)

    return code_template


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    """
    Create test user fixture (regular user).

    Returns a User model instance for testing.
    Email: test@user.com
    Password: testpass123
    Role: user
    """
    from app.models.user import User

    user = User(
        email="test@user.com",
        password_hash=get_password_hash("testpass123"),
        role="user"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def test_admin(db_session: AsyncSession):
    """
    Create test admin user fixture.

    Returns a User model instance with admin role for testing.
    Email: admin@test.com
    Password: adminpass123
    Role: admin
    """
    from app.models.user import User

    admin = User(
        email="admin@test.com",
        password_hash=get_password_hash("adminpass123"),
        role="admin"
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)

    return admin


@pytest_asyncio.fixture
async def auth_token(client: AsyncClient, test_admin):
    """
    Create authenticated admin token fixture.

    Logs in the test admin and returns the JWT access token.
    Use this for testing protected endpoints.

    Usage:
        async def test_protected_route(client: AsyncClient, auth_token: str):
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = await client.post("/api/v1/admin/algorithms", headers=headers, json=data)
    """
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "adminpass123"
    })
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def user_token(client: AsyncClient, test_user):
    """
    Create authenticated user token fixture.

    Logs in the test user (non-admin) and returns the JWT access token.
    Use this for testing user-level permissions.
    """
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@user.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    return response.json()["access_token"]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (no external dependencies)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (database, external services)"
    )
    config.addinivalue_line(
        "markers", "slow: Slow running tests"
    )
