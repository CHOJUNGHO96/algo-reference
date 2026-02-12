# Algo Reference - Development Guide

프로젝트: **알고리즘 참고 자료** 풀스택 애플리케이션
기술 스택: Python FastAPI (Backend) + React TypeScript (Frontend)

---

## 🏗️ 프로젝트 구조

```
algo-reference/
├── backend/              # Python FastAPI 백엔드
│   ├── app/
│   │   ├── api/         # API 엔드포인트 (라우터)
│   │   ├── core/        # 설정, 보안, 데이터베이스
│   │   ├── models/      # SQLAlchemy 모델
│   │   └── schemas/     # Pydantic 스키마
│   ├── alembic/         # 데이터베이스 마이그레이션
│   ├── tests/           # pytest 테스트
│   └── requirements.txt # Python 의존성
├── frontend/            # React TypeScript 프론트엔드
│   ├── src/
│   │   ├── components/  # 재사용 컴포넌트
│   │   ├── pages/       # 페이지 컴포넌트
│   │   ├── store/       # Redux 상태 관리
│   │   └── types/       # TypeScript 타입 정의
│   ├── package.json     # npm 의존성
│   └── vite.config.ts   # Vite 설정
└── docs/                # 프로젝트 문서
```

---

## 🔧 개발 워크플로우

### Backend (Python FastAPI)

#### 패키지 관리
- **항상 venv 사용**: `.venv` 가상 환경 활성화 후 작업
- **의존성 설치**: `pip install -r requirements.txt`
- **새 패키지 추가 시**: `requirements.txt`에 버전 명시

#### 개발 순서
1. 코드 변경
2. 타입 체크: `mypy backend/app/` (Python 타입 힌트 검증)
3. 테스트: `pytest backend/tests/`
4. 린트: `black backend/` (자동 포맷팅)
5. 서버 실행: `cd backend && uvicorn app.main:app --reload`

#### 데이터베이스 마이그레이션
```bash
# 새 마이그레이션 생성
cd backend
alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
alembic upgrade head

# 현재 리비전 확인
alembic current
```

#### API 개발 규칙
- **비동기 우선**: `async def` 사용, `await` 명시
- **의존성 주입**: FastAPI Depends() 활용
- **Pydantic 스키마**: 요청/응답 검증 필수
- **에러 처리**: HTTPException 사용
- **보안**: JWT 토큰 검증, SQL Injection 방지 (SQLAlchemy ORM)

### Frontend (React TypeScript)

#### 패키지 관리
- **항상 npm 사용**: `yarn`, `pnpm` 사용 금지
- **의존성 설치**: `npm install`
- **새 패키지 추가**: `npm install --save <package>`

#### 개발 순서
1. 코드 변경
2. 타입 체크: `npm run build` (TypeScript 컴파일)
3. 린트: `npm run lint`
4. 테스트: `npm run test:run`
5. 개발 서버: `npm run dev`

#### React 컴포넌트 규칙
- **함수형 컴포넌트**: `function Component() {}` 또는 `const Component = () => {}`
- **Hooks**: useState, useEffect, useCallback, useMemo 적절히 사용
- **Redux**: 전역 상태는 Redux Toolkit slices로 관리
- **폼**: React Hook Form + Zod validation
- **스타일**: Ant Design 컴포넌트 우선 사용

---

## 📝 코딩 컨벤션

### Backend (Python)

```python
# ✅ Good: 비동기 함수, 타입 힌트, Pydantic
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """사용자 생성 API"""
    # DB 로직
    new_user = User(**user_data.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# ❌ Bad: 동기 함수, 타입 힌트 없음
def create_user(user_data):
    # ...
```

**Python 규칙**:
- Type hints 필수: `def func(arg: str) -> int:`
- Docstring 작성: Google Style
- Black 포맷터 적용 (line length: 88)
- F-strings 사용: `f"Hello {name}"`
- 에러 처리: `try-except` 명시적 사용

### Frontend (TypeScript)

```typescript
// ✅ Good: 타입 정의, Zod validation, React Hook Form
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type UserFormData = z.infer<typeof userSchema>;

export function UserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
  });

  const onSubmit = async (data: UserFormData) => {
    // API 호출
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  );
}

// ❌ Bad: any 타입, validation 없음
export function UserForm() {
  const onSubmit = (data: any) => {
    // ...
  };
}
```

**TypeScript 규칙**:
- **`type` 선호, `interface` 자제**: 일관성 유지
- **`enum` 절대 금지**: 문자열 리터럴 유니온 사용
  ```typescript
  // ❌ Bad
  enum UserRole { Admin, User }

  // ✅ Good
  type UserRole = 'admin' | 'user';
  ```
- **Zod 스키마로 타입 정의**: 런타임 검증 + 타입 추론
- **`any` 타입 금지**: `unknown` 또는 구체적 타입 사용
- **컴포넌트 Props**: 명시적 타입 정의
  ```typescript
  type ButtonProps = {
    label: string;
    onClick: () => void;
    disabled?: boolean;
  };

  export function Button({ label, onClick, disabled }: ButtonProps) {
    // ...
  }
  ```

---

## 🧪 테스트 전략

### Backend (pytest)

```bash
# 전체 테스트 실행
pytest backend/tests/

# 특정 파일 테스트
pytest backend/tests/test_users.py

# 커버리지 리포트
pytest --cov=app --cov-report=html backend/tests/
```

**테스트 작성 규칙**:
- **비동기 테스트**: `@pytest.mark.asyncio` 사용
- **Fixture**: 공통 설정은 `conftest.py`에
- **Mock**: `unittest.mock` 또는 `pytest-mock` 사용
- **DB 테스트**: 테스트 DB 사용, 트랜잭션 롤백

### Frontend (Vitest)

```bash
# 전체 테스트 실행
npm run test:run

# Watch 모드
npm run test

# 커버리지
npm run test:coverage

# UI 모드
npm run test:ui
```

**테스트 작성 규칙**:
- **React Testing Library** 사용
- **유저 중심 테스트**: 실제 사용자 행동 시뮬레이션
- **Mock**: `vi.mock()` 사용
- **비동기 테스트**: `waitFor`, `findBy*` 사용

---

## 🚀 배포 및 실행

### Docker Compose로 전체 스택 실행

```bash
# 전체 스택 실행 (backend + frontend + PostgreSQL)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 종료
docker-compose down
```

### 개발 모드 (로컬)

```bash
# Backend
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (새 터미널)
cd frontend
npm run dev
```

---

## 🔒 보안 규칙

### Backend
- **환경 변수**: `.env` 파일 사용, `.gitignore`에 포함
- **비밀번호**: bcrypt 해싱 (passlib)
- **JWT**: SECRET_KEY 환경 변수로 관리
- **CORS**: 허용된 origin만 설정
- **SQL Injection**: SQLAlchemy ORM 사용 (raw query 자제)

### Frontend
- **API 키**: `.env` 파일, `VITE_` 접두사
- **토큰 저장**: localStorage 대신 httpOnly cookie 권장
- **XSS 방지**: React의 자동 이스케이핑 활용
- **CSRF**: API 요청에 CSRF 토큰 포함

---

## 📚 금지 사항

### Backend
- ❌ `print()` 사용 → ✅ `logging` 모듈 사용
- ❌ 동기 함수 사용 → ✅ `async def` 사용
- ❌ Type hints 생략 → ✅ 모든 함수에 타입 명시
- ❌ Raw SQL 쿼리 → ✅ SQLAlchemy ORM

### Frontend
- ❌ `console.log()` 프로덕션 코드 → ✅ 개발 중에만 사용
- ❌ `any` 타입 → ✅ 구체적 타입 또는 `unknown`
- ❌ `enum` 사용 → ✅ 문자열 리터럴 유니온
- ❌ `var` 키워드 → ✅ `const`, `let` 사용
- ❌ `== ` 비교 → ✅ `===` strict 비교

---

## 🔗 주요 링크

- **Backend API 문서**: http://localhost:8000/docs (Swagger UI)
- **Frontend 개발 서버**: http://localhost:3000
- **PostgreSQL**: localhost:5432

---

## 📖 추가 문서

- `backend/README.md`: Backend 상세 가이드
- `frontend/README.md`: Frontend 상세 가이드
- `docs/`: 프로젝트 설계 문서
- `issue/`: 이슈 해결 기록

---

**마지막 업데이트**: 2026-02-12
**관리자**: Algo Reference Team
