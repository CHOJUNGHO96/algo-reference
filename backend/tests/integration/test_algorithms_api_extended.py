"""
Extended integration tests for Algorithm API endpoints.

Comprehensive tests for:
- Pagination edge cases
- Multiple filter combinations
- Search ranking and relevance
- Sorting variations
- Code template inclusion
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_algorithms_pagination_first_page(client: AsyncClient, test_algorithm):
    """Test first page of pagination with page size 12"""
    response = await client.get("/api/v1/algorithms?page=1&size=12")

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 12
    assert data["total"] == 1
    assert len(data["items"]) == 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_algorithms_pagination_second_page_empty(client: AsyncClient, test_algorithm):
    """Test second page returns empty when only 1 algorithm exists"""
    response = await client.get("/api/v1/algorithms?page=2&size=12")

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["size"] == 12
    assert data["total"] == 1
    assert len(data["items"]) == 0  # No items on page 2


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_by_category_only(client: AsyncClient, test_algorithm, test_category):
    """Test filtering algorithms by category only"""
    response = await client.get(f"/api/v1/algorithms?category_id={test_category.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category"]["id"] == test_category.id
    assert data["items"][0]["category"]["name"] == "Two Pointer"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_by_difficulty_only(client: AsyncClient, test_algorithm, test_difficulty):
    """Test filtering algorithms by difficulty only"""
    response = await client.get(f"/api/v1/algorithms?difficulty_id={test_difficulty.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["difficulty"]["id"] == test_difficulty.id
    assert data["items"][0]["difficulty"]["name"] == "Medium"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_by_category_and_difficulty(
    client: AsyncClient,
    test_algorithm,
    test_category,
    test_difficulty
):
    """Test filtering algorithms by both category and difficulty"""
    response = await client.get(
        f"/api/v1/algorithms?category_id={test_category.id}&difficulty_id={test_difficulty.id}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category"]["id"] == test_category.id
    assert data["items"][0]["difficulty"]["id"] == test_difficulty.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_by_nonexistent_category(client: AsyncClient):
    """Test filtering by non-existent category returns no results"""
    response = await client.get("/api/v1/algorithms?category_id=9999")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_filter_by_nonexistent_difficulty(client: AsyncClient):
    """Test filtering by non-existent difficulty returns no results"""
    response = await client.get("/api/v1/algorithms?difficulty_id=9999")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_by_title_exact_match(client: AsyncClient, test_algorithm):
    """Test search with exact title match"""
    response = await client.get("/api/v1/algorithms?search=Two Pointer Technique")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Two Pointer Technique" in item["title"] for item in data["items"])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_by_title_partial_match(client: AsyncClient, test_algorithm):
    """Test search with partial title match"""
    response = await client.get("/api/v1/algorithms?search=pointer")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Pointer" in item["title"] for item in data["items"])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_by_concept_summary(client: AsyncClient, test_algorithm):
    """Test search matches concept_summary content"""
    response = await client.get("/api/v1/algorithms?search=indices")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    # Should match "indices" in concept_summary


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_case_insensitive(client: AsyncClient, test_algorithm):
    """Test search is case-insensitive"""
    response_lower = await client.get("/api/v1/algorithms?search=two pointer")
    response_upper = await client.get("/api/v1/algorithms?search=TWO POINTER")
    response_mixed = await client.get("/api/v1/algorithms?search=TwO pOiNtEr")

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    assert response_mixed.status_code == 200

    data_lower = response_lower.json()
    data_upper = response_upper.json()
    data_mixed = response_mixed.json()

    # All should return same results
    assert data_lower["total"] == data_upper["total"] == data_mixed["total"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_with_no_results(client: AsyncClient):
    """Test search with query that matches nothing"""
    response = await client.get("/api/v1/algorithms?search=xyznonexistent12345")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_empty_query_returns_all(client: AsyncClient, test_algorithm):
    """Test empty search query returns all published algorithms"""
    response = await client.get("/api/v1/algorithms?search=")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_combined_filter_category_difficulty_search(
    client: AsyncClient,
    test_algorithm,
    test_category,
    test_difficulty
):
    """Test combining category, difficulty, and search filters"""
    response = await client.get(
        f"/api/v1/algorithms?category_id={test_category.id}"
        f"&difficulty_id={test_difficulty.id}&search=pointer"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1

    # Verify all filters applied
    for item in data["items"]:
        assert item["category"]["id"] == test_category.id
        assert item["difficulty"]["id"] == test_difficulty.id
        assert "pointer" in item["title"].lower() or "pointer" in item["concept_summary"].lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sort_by_title_ascending(client: AsyncClient, db_session, test_category, test_difficulty):
    """Test sorting algorithms by title ascending"""
    from app.models.algorithm import Algorithm as AlgorithmModel

    # Create multiple algorithms with different titles
    algorithms = [
        AlgorithmModel(
            title="A First Algorithm",
            slug="a-first-algorithm",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary="Test A",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True
        ),
        AlgorithmModel(
            title="Z Last Algorithm",
            slug="z-last-algorithm",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary="Test Z",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True
        ),
    ]

    for alg in algorithms:
        db_session.add(alg)
    await db_session.commit()

    response = await client.get("/api/v1/algorithms?sort_by=title&order=asc")

    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data["items"]]

    # Verify ascending order
    assert titles == sorted(titles)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sort_by_title_descending(client: AsyncClient, db_session, test_category, test_difficulty):
    """Test sorting algorithms by title descending"""
    from app.models.algorithm import Algorithm as AlgorithmModel

    # Create multiple algorithms
    algorithms = [
        AlgorithmModel(
            title="A First Algorithm",
            slug="a-first-algorithm-desc",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary="Test A",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True
        ),
        AlgorithmModel(
            title="Z Last Algorithm",
            slug="z-last-algorithm-desc",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary="Test Z",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True
        ),
    ]

    for alg in algorithms:
        db_session.add(alg)
    await db_session.commit()

    response = await client.get("/api/v1/algorithms?sort_by=title&order=desc")

    assert response.status_code == 200
    data = response.json()
    titles = [item["title"] for item in data["items"]]

    # Verify descending order
    assert titles == sorted(titles, reverse=True)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sort_by_view_count(client: AsyncClient, db_session, test_category, test_difficulty):
    """Test sorting algorithms by view count"""
    from app.models.algorithm import Algorithm as AlgorithmModel

    # Create algorithms with different view counts
    algorithms = [
        AlgorithmModel(
            title="Popular Algorithm",
            slug="popular-algorithm",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary="Test",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True,
            view_count=1000
        ),
        AlgorithmModel(
            title="Unpopular Algorithm",
            slug="unpopular-algorithm",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary="Test",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True,
            view_count=10
        ),
    ]

    for alg in algorithms:
        db_session.add(alg)
    await db_session.commit()

    response = await client.get("/api/v1/algorithms?sort_by=view_count&order=desc")

    assert response.status_code == 200
    data = response.json()
    view_counts = [item["view_count"] for item in data["items"]]

    # Verify descending order (most viewed first)
    assert view_counts == sorted(view_counts, reverse=True)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_algorithm_includes_code_templates(
    client: AsyncClient,
    test_algorithm,
    test_code_template
):
    """Test get algorithm by slug includes code templates"""
    response = await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")

    assert response.status_code == 200
    data = response.json()

    # Verify code templates included
    assert "code_templates" in data
    assert len(data["code_templates"]) >= 1

    # Verify template structure
    template = data["code_templates"][0]
    assert "language" in template
    assert "code" in template
    assert template["language"]["name"] == "Python"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_algorithm_includes_all_8_sections(client: AsyncClient, test_algorithm):
    """Test get algorithm returns all 8 required sections"""
    response = await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")

    assert response.status_code == 200
    data = response.json()

    # Verify all 8 sections present
    required_fields = [
        "concept_summary",
        "core_formulas",
        "thought_process",
        "application_conditions",
        "time_complexity",
        "space_complexity",
        "problem_types",
        "common_mistakes"
    ]

    for field in required_fields:
        assert field in data
        assert data[field] is not None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_unpublished_algorithms_not_listed(client: AsyncClient, db_session, test_category, test_difficulty):
    """Test unpublished algorithms don't appear in public listing"""
    from app.models.algorithm import Algorithm as AlgorithmModel

    # Create unpublished algorithm
    unpublished = AlgorithmModel(
        title="Unpublished Algorithm",
        slug="unpublished-algorithm",
        category_id=test_category.id,
        difficulty_id=test_difficulty.id,
        concept_summary="This should not appear",
        time_complexity="O(1)",
        space_complexity="O(1)",
        is_published=False  # Not published
    )
    db_session.add(unpublished)
    await db_session.commit()

    # List all algorithms
    response = await client.get("/api/v1/algorithms")

    assert response.status_code == 200
    data = response.json()

    # Verify unpublished algorithm not in results
    titles = [item["title"] for item in data["items"]]
    assert "Unpublished Algorithm" not in titles


@pytest.mark.integration
@pytest.mark.asyncio
async def test_pagination_calculates_total_pages_correctly(
    client: AsyncClient,
    db_session,
    test_category,
    test_difficulty
):
    """Test pagination calculates total pages correctly"""
    from app.models.algorithm import Algorithm as AlgorithmModel

    # Create 25 algorithms (will require 3 pages at size=12)
    for i in range(25):
        alg = AlgorithmModel(
            title=f"Algorithm {i}",
            slug=f"algorithm-{i}",
            category_id=test_category.id,
            difficulty_id=test_difficulty.id,
            concept_summary=f"Summary {i}",
            time_complexity="O(1)",
            space_complexity="O(1)",
            is_published=True
        )
        db_session.add(alg)
    await db_session.commit()

    response = await client.get("/api/v1/algorithms?page=1&size=12")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 25
    assert data["pages"] == 3  # ceil(25 / 12) = 3
    assert len(data["items"]) == 12  # First page has 12 items
