---
name: algo-reference-database
description: 데이터베이스 연결 및 Alembic 마이그레이션. Use when working with database connections, migrations, or query optimization.
---

# Algo Reference Database Management

PostgreSQL 데이터베이스 연결, Alembic 마이그레이션, 쿼리 최적화 패턴입니다.

## 데이터베이스 연결

### 설정 (backend/app/core/database.py)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 연결 유효성 검사
    pool_recycle=3600    # 1시간마다 연결 재생성
)

# 비동기 세션 팩토리
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    """데이터베이스 세션 의존성"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 환경 변수 (.env)

```ini
DATABASE_URL=postgresql+asyncpg://postgres:password@192.168.164.1:5432/postgres
POSTGRES_SCHEMA=algo
```

## Alembic 마이그레이션

### 초기 설정 (alembic.ini)

```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://postgres:password@localhost:5432/postgres

[post_write_hooks]
hooks = black
black.type = console_scripts
black.entrypoint = black
```

### env.py 설정

```python
# backend/alembic/env.py
import asyncio
import os
from pathlib import Path
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.database import Base
from app.models import *  # 모든 모델 import

# .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

config = context.config
fileConfig(config.config_file_name)

# 환경 변수에서 DATABASE_URL 읽기
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

async def run_async_migrations():
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={
            "timeout": 30,
            "server_settings": {
                "search_path": os.getenv("POSTGRES_SCHEMA", "public"),
            },
        },
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 마이그레이션 명령어

```bash
# 새 마이그레이션 생성 (autogenerate)
cd backend
alembic revision --autogenerate -m "add user table"

# 마이그레이션 적용
alembic upgrade head

# 1단계 롤백
alembic downgrade -1

# 현재 리비전 확인
alembic current

# 마이그레이션 히스토리
alembic history

# 특정 리비전으로 이동
alembic upgrade <revision_id>
```

## 쿼리 최적화

### 1. N+1 쿼리 문제 해결

```python
# ❌ Bad: N+1 쿼리
users = await db.execute(select(User))
for user in users.scalars():
    posts = await db.execute(select(Post).where(Post.user_id == user.id))
    # N번의 추가 쿼리 발생

# ✅ Good: selectinload로 한 번에 로드
from sqlalchemy.orm import selectinload

users = await db.execute(
    select(User).options(selectinload(User.posts))
)
for user in users.scalars():
    posts = user.posts  # 추가 쿼리 없음
```

### 2. 인덱스 사용

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # 인덱스
    created_at = Column(DateTime, index=True)        # 인덱스

    # 복합 인덱스
    __table_args__ = (
        Index('idx_email_created', 'email', 'created_at'),
    )
```

### 3. 부분 쿼리 (특정 컬럼만)

```python
# ✅ Good: 필요한 컬럼만 조회
result = await db.execute(
    select(User.id, User.email).where(User.is_active == True)
)
users = result.all()
```

### 4. 배치 삽입

```python
# ❌ Bad: 개별 삽입
for data in user_data_list:
    user = User(**data)
    db.add(user)
    await db.commit()  # N번의 커밋

# ✅ Good: 배치 삽입
users = [User(**data) for data in user_data_list]
db.add_all(users)
await db.commit()  # 1번의 커밋
```

### 5. 트랜잭션 관리

```python
async def transfer_money(from_user_id: int, to_user_id: int, amount: int, db: AsyncSession):
    async with db.begin():  # 트랜잭션 시작
        # 출금
        from_user = await db.get(User, from_user_id)
        from_user.balance -= amount

        # 입금
        to_user = await db.get(User, to_user_id)
        to_user.balance += amount

        # 자동 커밋 또는 롤백
```

## Connection Pool 설정

```python
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,          # 기본 연결 수
    max_overflow=20,       # 추가 연결 수 (최대 30)
    pool_timeout=30,       # 연결 대기 시간 (초)
    pool_recycle=3600,     # 연결 재생성 주기 (1시간)
    pool_pre_ping=True,    # 연결 유효성 검사
    echo=False             # SQL 로깅 (개발 시만 True)
)
```

## 데이터베이스 백업

```bash
# PostgreSQL 백업
pg_dump -h localhost -U postgres -d dbname > backup.sql

# 복원
psql -h localhost -U postgres -d dbname < backup.sql

# Docker 환경에서 백업
docker exec -t postgres-container pg_dump -U postgres dbname > backup.sql
```

## 트러블슈팅

### 마이그레이션 충돌

```bash
# 현재 상태 확인
alembic current

# 히스토리 확인
alembic history

# 헤드 병합 (여러 브랜치)
alembic merge heads -m "merge branches"
```

### 연결 풀 고갈

```python
# 연결 상태 확인
print(engine.pool.status())

# 연결 재설정
await engine.dispose()
```

## 자주 사용하는 명령어

```bash
# 마이그레이션 생성 및 적용
cd backend && alembic revision --autogenerate -m "description" && alembic upgrade head

# DB 리셋 (주의!)
alembic downgrade base && alembic upgrade head

# 마이그레이션 상태 확인
alembic current
alembic history
```

## 관련 스킬

- algo-reference-models: SQLAlchemy 모델
- algo-reference-api: API 엔드포인트
