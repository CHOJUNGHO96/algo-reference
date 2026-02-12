"""
Integration tests for Algorithm API endpoints.

Tests the following endpoints:
- GET /api/v1/algorithms - List algorithms with pagination
- GET /api/v1/algorithms/{slug} - Get algorithm by slug
- POST /api/v1/admin/algorithms - Create algorithm (admin only)
- PUT /api/v1/admin/algorithms/{slug} - Update algorithm (admin only)
- DELETE /api/v1/admin/algorithms/{slug} - Delete algorithm (admin only)
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_algorithms_empty(client: AsyncClient):
    """Test listing algorithms when database is empty."""
    response = await client.get("/api/v1/algorithms")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["page"] == 1
    assert data["page_size"] == 20


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_algorithms_with_data(client: AsyncClient, test_algorithm):
    """Test listing algorithms with existing data."""
    response = await client.get("/api/v1/algorithms")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Two Pointer Technique"
    assert data["items"][0]["slug"] == "two-pointer-technique"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_algorithms_pagination(client: AsyncClient, test_algorithm):
    """Test pagination of algorithm list."""
    response = await client.get("/api/v1/algorithms?page=1&page_size=10")

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_algorithm_by_slug(client: AsyncClient, test_algorithm):
    """Test retrieving algorithm by slug."""
    response = await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Two Pointer Technique"
    assert data["slug"] == "two-pointer-technique"
    assert data["time_complexity"] == "O(n)"
    assert data["space_complexity"] == "O(1)"
    assert data["is_published"] is True
    assert "category" in data
    assert "difficulty" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_algorithm_not_found(client: AsyncClient):
    """Test 404 for non-existent algorithm."""
    response = await client.get("/api/v1/algorithms/non-existent-slug")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_algorithm_view_count_increment(client: AsyncClient, test_algorithm, db_session):
    """Test that getting an algorithm increments view count."""
    initial_count = test_algorithm.view_count

    # First view
    response = await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")
    assert response.status_code == 200

    # Refresh to get updated count
    await db_session.refresh(test_algorithm)
    assert test_algorithm.view_count == initial_count + 1

    # Second view
    await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")
    await db_session.refresh(test_algorithm)
    assert test_algorithm.view_count == initial_count + 2


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_algorithm_admin(
    client: AsyncClient,
    auth_token: str,
    test_category,
    test_difficulty
):
    """Test creating algorithm with admin authentication."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Binary Search",
        "category_id": test_category.id,
        "difficulty_id": test_difficulty.id,
        "concept_summary": "Binary search is a divide-and-conquer algorithm...",
        "core_formulas": "mid = (left + right) // 2",
        "thought_process": "1. Find middle\n2. Compare with target\n3. Narrow search space",
        "application_conditions": "Sorted array required",
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "problem_types": "Search in sorted array, find first/last occurrence",
        "common_mistakes": "Integer overflow in mid calculation",
        "is_published": True
    }

    response = await client.post(
        "/api/v1/admin/algorithms",
        json=payload,
        headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Binary Search"
    assert data["slug"] == "binary-search"
    assert data["time_complexity"] == "O(log n)"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_algorithm_unauthorized(client: AsyncClient, test_category, test_difficulty):
    """Test creating algorithm without authentication fails."""
    payload = {
        "title": "Test Algorithm",
        "category_id": test_category.id,
        "difficulty_id": test_difficulty.id,
        "concept_summary": "Test",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    }

    response = await client.post("/api/v1/admin/algorithms", json=payload)

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_algorithm_validation_error(client: AsyncClient, auth_token: str):
    """Test creating algorithm with invalid data returns 422."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "",  # Empty title should fail validation
        "category_id": 999,  # Non-existent category
        "difficulty_id": 999  # Non-existent difficulty
    }

    response = await client.post(
        "/api/v1/admin/algorithms",
        json=payload,
        headers=headers
    )

    assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_algorithm_admin(client: AsyncClient, auth_token: str, test_algorithm):
    """Test updating algorithm with admin authentication."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Updated Two Pointer Technique",
        "concept_summary": "Updated summary...",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"  # Changed from O(1)
    }

    response = await client.put(
        f"/api/v1/admin/algorithms/{test_algorithm.slug}",
        json=payload,
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Two Pointer Technique"
    assert data["space_complexity"] == "O(n)"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_algorithm_not_found(client: AsyncClient, auth_token: str):
    """Test updating non-existent algorithm returns 404."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"title": "Updated Title"}

    response = await client.put(
        "/api/v1/admin/algorithms/non-existent-slug",
        json=payload,
        headers=headers
    )

    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_algorithm_admin(client: AsyncClient, auth_token: str, test_algorithm):
    """Test deleting algorithm with admin authentication."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.delete(
        f"/api/v1/admin/algorithms/{test_algorithm.slug}",
        headers=headers
    )

    assert response.status_code == 204

    # Verify algorithm is deleted
    get_response = await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")
    assert get_response.status_code == 404


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_algorithm_unauthorized(client: AsyncClient, test_algorithm):
    """Test deleting algorithm without authentication fails."""
    response = await client.delete(f"/api/v1/admin/algorithms/{test_algorithm.slug}")

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_algorithms_by_category(
    client: AsyncClient,
    test_algorithm,
    test_category
):
    """Test filtering algorithms by category."""
    response = await client.get(f"/api/v1/algorithms?category_id={test_category.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category"]["id"] == test_category.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_algorithms_by_difficulty(
    client: AsyncClient,
    test_algorithm,
    test_difficulty
):
    """Test filtering algorithms by difficulty."""
    response = await client.get(f"/api/v1/algorithms?difficulty_id={test_difficulty.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["difficulty"]["id"] == test_difficulty.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_algorithms(client: AsyncClient, test_algorithm):
    """Test full-text search of algorithms."""
    response = await client.get("/api/v1/algorithms?search=two pointer")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Two Pointer" in item["title"] for item in data["items"])
