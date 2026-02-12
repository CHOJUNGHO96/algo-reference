---
name: algo-reference-api
description: FastAPI 라우터 및 엔드포인트 패턴. Use when creating or modifying API endpoints, routes, or HTTP handlers.
---

# Algo Reference API Patterns

FastAPI 라우터 및 엔드포인트 작성 패턴입니다.

## 라우터 구조

```python
# backend/app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """사용자 생성"""
    # 중복 이메일 확인
    existing_user = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 새 사용자 생성
    new_user = User(**user_data.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """사용자 조회"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[UserResponse]:
    """사용자 목록 조회"""
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return users

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """사용자 수정"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 권한 확인 (본인 또는 관리자만)
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # 업데이트
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """사용자 삭제"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 권한 확인
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    await db.delete(user)
    await db.commit()
```

## 핵심 패턴

### 1. 비동기 함수 사용

```python
# ✅ Good: 비동기
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# ❌ Bad: 동기
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### 2. 의존성 주입

```python
# DB 세션 의존성
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# 현재 사용자 의존성
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # JWT 토큰 검증
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user
```

### 3. Response 모델 정의

```python
# ✅ Good: Pydantic response model
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    return user  # 자동으로 UserResponse로 직렬화

# ❌ Bad: 직접 dict 반환
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    return {"id": user.id, "email": user.email}  # 수동 직렬화
```

### 4. HTTPException 사용

```python
# ✅ Good: 명확한 에러 처리
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# ❌ Bad: 일반 Exception
if not user:
    raise Exception("User not found")
```

### 5. 페이지네이션

```python
@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
    )
    return result.scalars().all()
```

## 라우터 등록

```python
# backend/app/main.py
from fastapi import FastAPI
from app.api.routes import users, auth

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
```

## API 문서

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 자주 사용하는 명령어

```bash
# 개발 서버 실행
cd backend && uvicorn app.main:app --reload

# API 테스트
curl http://localhost:8000/api/v1/users

# OpenAPI 스펙 다운로드
curl http://localhost:8000/openapi.json > api-contract.json
```

## 관련 스킬

- algo-reference-models: SQLAlchemy 모델
- algo-reference-database: DB 연결 및 쿼리
