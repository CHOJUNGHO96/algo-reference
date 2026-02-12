# Algorithm Reference Platform - Testing Guide

This directory contains all testing infrastructure for the Algorithm Reference Platform.

## Directory Structure

```
tests/
├── e2e/                          # End-to-end tests with Playwright
│   ├── specs/                    # Test specifications
│   │   ├── search-and-view.spec.ts
│   │   ├── admin-crud.spec.ts
│   │   └── navigation.spec.ts
│   ├── fixtures/                 # Test data fixtures
│   │   └── test-data.ts
│   ├── playwright.config.ts      # Playwright configuration
│   └── package.json              # E2E test dependencies
└── README.md                     # This file
```

Backend and frontend tests are located in their respective directories:
- **Backend Tests**: `backend/tests/`
- **Frontend Tests**: `frontend/src/**/__tests__/`

## Quick Start

### Backend Tests (pytest)

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/integration/test_algorithms_api.py

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run in parallel (faster)
pytest -n auto
```

### Frontend Tests (Vitest)

```bash
# Install dependencies
cd frontend
npm install

# Run tests in watch mode
npm test

# Run tests once
npm run test:run

# Run with coverage
npm run test:coverage

# Run with UI
npm run test:ui

# Run specific test file
npm test -- AlgorithmCard.test.tsx
```

### E2E Tests (Playwright)

```bash
# Install dependencies and browsers
cd tests/e2e
npm install
npm run install  # Installs browser binaries

# Run all E2E tests
npm test

# Run in headed mode (see browser)
npm run test:headed

# Run with UI mode (interactive)
npm run test:ui

# Run specific browser
npm run test:chromium
npm run test:firefox
npm run test:webkit

# Run mobile tests
npm run test:mobile

# Debug mode
npm run test:debug

# View test report
npm run report
```

## Test Categories

### Backend Tests

**Unit Tests** (`backend/tests/unit/`):
- `test_security.py`: Password hashing, JWT tokens
- `test_models.py`: SQLAlchemy model validation
- `test_schemas.py`: Pydantic schema validation

**Integration Tests** (`backend/tests/integration/`):
- `test_algorithms_api.py`: Algorithm CRUD endpoints
- `test_auth_api.py`: Authentication flows
- `test_categories_api.py`: Category endpoints
- `test_search.py`: Search functionality

### Frontend Tests

**Component Tests** (`frontend/src/components/__tests__/`):
- `AlgorithmCard.test.tsx`: Algorithm card component
- `CodeBlock.test.tsx`: Code display component
- `Sidebar.test.tsx`: Navigation sidebar
- `Header.test.tsx`: Page header

**Page Tests** (`frontend/src/pages/__tests__/`):
- `AlgorithmListPage.test.tsx`: List page
- `AlgorithmDetailPage.test.tsx`: Detail page
- `AdminLoginPage.test.tsx`: Login page

### E2E Tests

**Critical User Flows** (`tests/e2e/specs/`):
1. **search-and-view.spec.ts**: Search and view algorithm
2. **admin-crud.spec.ts**: Admin CRUD operations
3. **navigation.spec.ts**: Category navigation
4. **theme.spec.ts**: Dark mode persistence

## Writing Tests

### Backend Test Example

```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_algorithm(client: AsyncClient, test_algorithm):
    """Test retrieving algorithm by slug."""
    response = await client.get(f"/api/v1/algorithms/{test_algorithm.slug}")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Two Pointer Technique"
```

### Frontend Test Example

```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AlgorithmCard from '../AlgorithmCard';

describe('AlgorithmCard', () => {
  it('renders algorithm title', () => {
    render(<AlgorithmCard algorithm={mockAlgorithm} />);
    expect(screen.getByText('Two Pointer Technique')).toBeInTheDocument();
  });
});
```

### E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test('user can search algorithms', async ({ page }) => {
  await page.goto('/');
  await page.fill('[data-testid="search-input"]', 'Two Pointer');
  await expect(page.locator('[data-testid="algorithm-card"]').first()).toBeVisible();
});
```

## Test Fixtures

### Backend Fixtures (pytest)

Available fixtures in `backend/tests/conftest.py`:
- `db_session`: Clean database session
- `client`: Test HTTP client
- `auth_token`: Admin JWT token
- `user_token`: User JWT token
- `test_algorithm`: Sample algorithm
- `test_category`: Sample category
- `test_difficulty`: Sample difficulty
- `test_language`: Sample language
- `test_user`: Regular user
- `test_admin`: Admin user

### Frontend Fixtures

Mock data helpers in test files:
- `renderWithRouter()`: Render component with React Router
- Mock algorithm objects
- Mock API responses (using MSW if needed)

### E2E Fixtures

Test data in `tests/e2e/fixtures/test-data.ts`:
- `testAlgorithm`: Sample algorithm data
- `testAdmin`: Admin credentials
- `newAlgorithm`: Data for creating algorithm
- `categories`: Category list
- `difficulties`: Difficulty levels

## Coverage Reports

### Backend Coverage

```bash
cd backend
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

Target: **≥80% line coverage**

### Frontend Coverage

```bash
cd frontend
npm run test:coverage
# Open coverage/index.html in browser
```

Target: **≥75% line coverage**

## CI/CD Integration

Tests run automatically on GitHub Actions:
- **Pull Requests**: All tests must pass
- **Main Branch**: Full test suite + coverage reports
- **Nightly**: E2E tests across all browsers

See `.github/workflows/test.yml` for configuration.

## Troubleshooting

### Backend Tests

**Database connection errors**:
```bash
# Ensure PostgreSQL is running
docker-compose up -d postgres

# Create test database
createdb algoref_test
```

**Import errors**:
```bash
# Ensure you're in backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

### Frontend Tests

**Module not found errors**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Vitest hanging**:
```bash
# Run without watch mode
npm run test:run
```

### E2E Tests

**Browser not installed**:
```bash
cd tests/e2e
npx playwright install chromium firefox webkit
```

**Tests timing out**:
- Increase timeout in `playwright.config.ts`
- Check if dev server is running (`npm run dev`)
- Use `--headed` mode to see what's happening

**Port already in use**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## Best Practices

### General
- Write descriptive test names that explain the scenario
- Follow AAA pattern: Arrange, Act, Assert
- One assertion per test (when possible)
- Use data-testid attributes for E2E selectors
- Mock external dependencies in unit tests
- Use real services in integration tests

### Backend
- Always use `async/await` with `pytest-asyncio`
- Wrap tests in transactions for database isolation
- Use fixtures for common test data
- Test both success and error cases
- Validate HTTP status codes and response schemas

### Frontend
- Use React Testing Library queries (getByRole, getByText)
- Test user behavior, not implementation details
- Avoid testing third-party library internals
- Use user-event for realistic interactions
- Test accessibility (aria-labels, roles)

### E2E
- Use stable selectors (data-testid preferred)
- Wait for elements with proper timeout strategies
- Test critical user journeys only
- Keep tests independent (no shared state)
- Use page object pattern for complex flows
- Take screenshots on failure for debugging

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Strategy Document](../docs/testing-strategy.md)
