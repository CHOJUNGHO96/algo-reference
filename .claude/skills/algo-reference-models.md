---
name: algo-reference-models
description: SQLAlchemy 모델 및 Pydantic 스키마 패턴. Use when defining database models, schemas, or data validation.
---

# Algo Reference Models & Schemas

SQLAlchemy 모델과 Pydantic 스키마 작성 패턴입니다.

## SQLAlchemy 모델

### 기본 모델

```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 관계 설정

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 관계
    author = relationship("User", back_populates="posts")

class User(Base):
    # ... 기존 필드
    posts = relationship("Post", back_populates="author")
```

## Pydantic 스키마

### Request/Response 스키마

```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """사용자 생성 요청"""
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    """사용자 수정 요청"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    """사용자 응답"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 모델 → Pydantic 변환
```

### 중첩 스키마

```python
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: UserResponse  # 중첩된 사용자 정보

    class Config:
        from_attributes = True

class UserWithPosts(UserResponse):
    posts: List[PostResponse] = []
```

## 핵심 패턴

### 1. 비밀번호 해싱

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    # ... 필드

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
```

### 2. 타임스탬프 자동 설정

```python
created_at = Column(DateTime(timezone=True), server_default=func.now())
updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 3. Soft Delete

```python
class User(Base):
    # ... 필드
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

### 4. 유효성 검증 (Pydantic Validator)

```python
from pydantic import validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v
```

## 데이터베이스 설정

```python
# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

## 마이그레이션

```bash
# 새 마이그레이션 생성
cd backend && alembic revision --autogenerate -m "add user table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

## 자주 사용하는 쿼리 패턴

### 1. 단일 조회

```python
user = await db.get(User, user_id)
```

### 2. 필터링

```python
result = await db.execute(
    select(User).where(User.email == email)
)
user = result.scalar_one_or_none()
```

### 3. 여러 조건

```python
result = await db.execute(
    select(User).where(
        User.is_active == True,
        User.email.like("%@example.com")
    )
)
users = result.scalars().all()
```

### 4. 정렬 및 페이지네이션

```python
result = await db.execute(
    select(User)
    .order_by(User.created_at.desc())
    .offset(skip)
    .limit(limit)
)
users = result.scalars().all()
```

### 5. Join

```python
result = await db.execute(
    select(Post)
    .join(User)
    .where(User.id == user_id)
)
posts = result.scalars().all()
```

## 관련 스킬

- algo-reference-api: API 엔드포인트
- algo-reference-database: DB 연결 및 마이그레이션
