---
name: algo-reference-architecture
description: 프로젝트 전체 아키텍처 및 폴더 구조. Use when working with project structure, architecture decisions, or module organization.
---

# Algo Reference Architecture

알고리즘 참고 자료 프로젝트의 전체 아키텍처 및 설계 원칙입니다.

## 프로젝트 구조

```
algo-reference/
├── backend/              # Python FastAPI 백엔드
│   ├── app/
│   │   ├── api/         # API 라우터 (엔드포인트)
│   │   ├── core/        # 핵심 설정 (config, security, database)
│   │   ├── models/      # SQLAlchemy 데이터베이스 모델
│   │   └── schemas/     # Pydantic 요청/응답 스키마
│   ├── alembic/         # 데이터베이스 마이그레이션
│   └── tests/           # Backend 테스트
├── frontend/            # React TypeScript 프론트엔드
│   └── src/
│       ├── components/  # 재사용 가능한 컴포넌트
│       ├── pages/       # 페이지 컴포넌트
│       ├── store/       # Redux 상태 관리
│       └── types/       # TypeScript 타입 정의
└── docs/                # 프로젝트 문서
```

## 아키텍처 패턴

### Backend (MVC 패턴)

**계층 구조**:
1. **API Layer** (`app/api/routes/`)
   - FastAPI 라우터
   - HTTP 요청/응답 처리
   - 의존성 주입

2. **Schema Layer** (`app/schemas/`)
   - Pydantic 모델
   - 요청/응답 검증
   - 데이터 직렬화

3. **Model Layer** (`app/models/`)
   - SQLAlchemy ORM 모델
   - 데이터베이스 스키마 정의
   - 관계 설정

4. **Core Layer** (`app/core/`)
   - 설정 관리
   - 보안 (JWT, 비밀번호)
   - 데이터베이스 연결

**의존성 방향**: API → Schemas → Models → Core

### Frontend (Component 기반)

**계층 구조**:
1. **Pages** (`src/pages/`)
   - 라우트별 페이지 컴포넌트
   - 레이아웃 구성

2. **Components** (`src/components/`)
   - 재사용 가능한 UI 컴포넌트
   - Ant Design 활용

3. **Store** (`src/store/`)
   - Redux Toolkit slices
   - 전역 상태 관리

4. **Types** (`src/types/`)
   - TypeScript 인터페이스/타입
   - API 응답 타입

**의존성 방향**: Pages → Components → Store/Types

## 핵심 원칙

### 1. 관심사 분리 (Separation of Concerns)
- API 라우터는 HTTP만 처리
- 비즈니스 로직은 별도 모듈로 분리 (추후)
- 데이터베이스 접근은 Models를 통해서만

### 2. 의존성 주입 (Dependency Injection)
- FastAPI Depends() 활용
- DB 세션, 인증 등을 의존성으로 주입
- 테스트 시 Mock 객체로 교체 가능

### 3. 타입 안전성 (Type Safety)
- Backend: Python Type Hints + Pydantic
- Frontend: TypeScript strict mode
- API 계약: OpenAPI 스펙

### 4. 비동기 우선 (Async First)
- Backend: `async def` 함수 사용
- Database: SQLAlchemy async
- Frontend: async/await 활용

## 모듈 간 통신

### Backend ↔ Frontend

```
Frontend (React)
   ↓ HTTP Request (JSON)
Backend API (FastAPI)
   ↓ SQL Query (ORM)
Database (PostgreSQL)
   ↑ SQL Result
Backend API
   ↑ HTTP Response (JSON)
Frontend (React)
```

### 인증 흐름

```
1. Frontend → POST /api/v1/auth/login
2. Backend → JWT 토큰 생성
3. Backend → 토큰 반환
4. Frontend → localStorage 저장
5. Frontend → 모든 요청에 Authorization 헤더 포함
6. Backend → 토큰 검증 (Depends(get_current_user))
```

## 파일 명명 규칙

### Backend (Python)
- 모듈: `snake_case.py` (예: `user_routes.py`)
- 클래스: `PascalCase` (예: `UserCreate`)
- 함수: `snake_case` (예: `create_user`)
- 상수: `UPPER_SNAKE_CASE` (예: `SECRET_KEY`)

### Frontend (TypeScript)
- 컴포넌트: `PascalCase.tsx` (예: `UserForm.tsx`)
- 훅: `use` 접두사 (예: `useAuth.ts`)
- 유틸리티: `camelCase.ts` (예: `formatDate.ts`)
- 타입: `type` 또는 `PascalCase` (예: `UserFormData`)

## 자주 사용하는 명령어

### 개발 서버 실행

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

### 테스트

```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd frontend && npm run test:run
```

### 마이그레이션

```bash
# 새 마이그레이션 생성
cd backend && alembic revision --autogenerate -m "description"

# 마이그레이션 적용
cd backend && alembic upgrade head
```

## 추가 정보

- Backend 상세: `backend/README.md`
- Frontend 상세: `frontend/README.md`
- API 스펙: `api-contract.yaml`
