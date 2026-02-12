---
name: algo-reference-testing
description: 테스트 패턴 및 실행 방법. Use when writing tests, debugging test failures, or improving test coverage.
---

# Algo Reference Testing Patterns

Backend (pytest) 및 Frontend (Vitest) 테스트 패턴과 베스트 프랙티스입니다.

## Backend Testing (pytest)

### 테스트 구조

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.user import User
from app.core.database import get_db

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db: AsyncSession):
    """사용자 생성 테스트"""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "password": "securePassword123",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```

### Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

@pytest_asyncio.fixture
async def db():
    """테스트 데이터베이스 세션"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db):
    """테스트 클라이언트"""
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

### 테스트 실행

```bash
# 전체 테스트
pytest backend/tests/ -v

# 특정 파일
pytest backend/tests/test_users.py -v

# Coverage
pytest backend/tests/ --cov=app --cov-report=html

# 병렬 실행
pytest backend/tests/ -n auto
```

## Frontend Testing (Vitest + React Testing Library)

### 컴포넌트 테스트

```typescript
// src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders with label', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button label="Click me" onClick={handleClick} />);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button label="Click me" onClick={() => {}} disabled />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### 비동기 테스트

```typescript
// src/pages/UserList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { UserList } from './UserList';

vi.mock('../services/api', () => ({
  fetchUsers: vi.fn(() => Promise.resolve([
    { id: 1, name: 'User 1' },
    { id: 2, name: 'User 2' }
  ]))
}));

describe('UserList Page', () => {
  it('loads and displays users', async () => {
    render(<UserList />);

    // 로딩 상태 확인
    expect(screen.getByText('Loading...')).toBeInTheDocument();

    // 데이터 로드 대기
    await waitFor(() => {
      expect(screen.getByText('User 1')).toBeInTheDocument();
      expect(screen.getByText('User 2')).toBeInTheDocument();
    });
  });
});
```

### 테스트 실행

```bash
# Watch 모드
cd frontend && npm run test

# 1회 실행
cd frontend && npm run test:run

# Coverage
cd frontend && npm run test:coverage

# UI 모드
cd frontend && npm run test:ui
```

## 테스트 패턴

### AAA 패턴 (Arrange-Act-Assert)

```python
async def test_user_login():
    # Arrange: 테스트 데이터 준비
    user_data = {"email": "test@example.com", "password": "password123"}

    # Act: 테스트 실행
    response = await client.post("/api/v1/auth/login", json=user_data)

    # Assert: 결과 검증
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Given-When-Then

```typescript
describe('User Login Flow', () => {
  it('should login successfully with valid credentials', async () => {
    // Given: 유효한 사용자 정보
    const credentials = { email: 'user@example.com', password: 'pass123' };

    // When: 로그인 시도
    const response = await login(credentials);

    // Then: 성공 응답 확인
    expect(response.status).toBe(200);
    expect(response.data.token).toBeDefined();
  });
});
```

## Mock 사용

### Backend (unittest.mock)

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_email():
    with patch('app.services.email.send_email', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = True

        result = await notify_user("test@example.com", "Message")

        assert result is True
        mock_send.assert_called_once_with("test@example.com", "Message")
```

### Frontend (vi.mock)

```typescript
vi.mock('../services/api', () => ({
  fetchUser: vi.fn((id: number) => Promise.resolve({ id, name: 'Test User' }))
}));

test('loads user data', async () => {
  const user = await fetchUser(1);
  expect(user).toEqual({ id: 1, name: 'Test User' });
});
```

## 커버리지 목표

- **Unit Tests**: 80% 이상
- **Integration Tests**: 주요 API 엔드포인트 모두 커버
- **E2E Tests**: 핵심 사용자 플로우 (로그인, 주요 기능)

## 자주 사용하는 명령어

```bash
# Backend 테스트 + Coverage
cd backend && pytest tests/ --cov=app --cov-report=html

# Frontend 테스트 + Coverage
cd frontend && npm run test:coverage

# 특정 테스트만 실행
pytest backend/tests/test_users.py::test_create_user -v

# 실패한 테스트만 재실행
pytest --lf
```

## 관련 문서

- pytest: https://docs.pytest.org/
- Vitest: https://vitest.dev/
- React Testing Library: https://testing-library.com/
