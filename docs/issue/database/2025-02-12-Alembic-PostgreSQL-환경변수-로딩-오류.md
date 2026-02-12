# Alembic PostgreSQL 환경변수 로딩 오류 - WinError 10054 및 ConnectionDoesNotExistError

**날짜**: 2025-02-12
**카테고리**: Database | Backend
**심각도**: High
**상태**: ✅ 해결됨

---

## 📋 문제 상황

FastAPI 백엔드에서 Alembic을 사용하여 PostgreSQL 마이그레이션을 실행할 때, 연결 오류가 발생했습니다. 애플리케이션에서는 정상적으로 PostgreSQL에 연결되지만, Alembic 마이그레이션 명령어(`alembic upgrade head`)를 실행하면 원격 호스트 연결 오류가 발생합니다.

### 에러 메시지

```
WinError 10054: 현재 연결은 원격 호스트에 의해 강제로 끊겼습니다.
```

또는

```
asyncpg.exceptions.ConnectionDoesNotExistError: no connection record found for connection 'default'
```

### 재현 방법

1. 프로젝트 루트 디렉토리에서 Alembic 마이그레이션 실행:
   ```bash
   cd backend
   alembic upgrade head
   ```

2. 출력되는 에러 메시지 확인

3. PostgreSQL 연결 로그에서 연결 실패 확인

### 증상

- **연결 거부**: PostgreSQL 서버(192.168.164.1:5432)로부터 강제 연결 종료
- **잘못된 호스트**: `alembic.ini`에 하드코딩된 `localhost:5432`로 연결 시도
- **속성 접근 오류**: `asyncpg` 드라이버에서 연결 객체 없음으로 인한 속성 접근 실패
- **차이점**: FastAPI 앱은 정상 작동하지만, Alembic만 오류 발생

### 발생 환경

- **OS**: Windows 10 Pro 10.0.19045
- **PostgreSQL**: 192.168.164.1:5432 (원격 서버)
- **Python 버전**: 3.11+
- **주요 패키지**:
  - SQLAlchemy 2.0+
  - alembic 1.10+
  - asyncpg 0.27+
  - python-dotenv 0.19+
- **구조**: 환경별 `.env` 파일 기반 설정 (FastAPI용)

---

## 🔍 원인 분석

### 근본 원인

**Alembic은 FastAPI와 달리 `.env` 파일을 자동으로 로드하지 않으므로, `env.py`에서 `os.getenv("DATABASE_URL")`을 호출할 때 None을 반환하여 `alembic.ini`의 잘못된 하드코딩된 URL로 폴백합니다.**

### 상세 분석

1. **환경 변수 로딩 실패**
   - 현상: `backend/alembic/env.py`에서 `os.getenv("DATABASE_URL")`이 None 반환
   - 원인: `.env` 파일이 Python 코드에 의해 명시적으로 로드되지 않음
   - 영향: 올바른 데이터베이스 URL을 사용할 수 없게 됨

2. **잘못된 폴백 URL 사용**
   - 현상: `alembic.ini`의 `sqlalchemy.url = postgresql://localhost/algoref` 사용
   - 원인: 환경 변수 로딩 실패 시 기본값으로 설정된 하드코딩된 URL
   - 영향: 실제 데이터베이스 서버(192.168.164.1:5432)가 아닌 로컬호스트로 연결 시도

3. **연결 실패**
   - 현상: 원격 호스트가 강제로 연결 종료 (`WinError 10054`)
   - 원인: 존재하지 않는 로컬 PostgreSQL 서버로 연결 시도
   - 영향: 마이그레이션 작업 불가, 명확한 오류 메시지 부재

### 잘못된 가정 또는 설정

- **가정/설정 1**: Alembic도 FastAPI처럼 자동으로 `.env` 파일을 로드할 것이다
  - 예상: 환경 변수 자동 설정
  - 실제: 명시적 로딩 필요 (python-dotenv 사용)

- **가정/설정 2**: `alembic.ini`의 하드코딩된 URL이 실제 환경에서 사용되지 않을 것이다
  - 예상: 환경 변수 기반 URL만 사용됨
  - 실제: 환경 변수 로딩 실패 시 폴백으로 사용됨

---

## ✅ 해결 방법

### 개요

Alembic의 `env.py`에서 `python-dotenv`를 사용하여 `.env` 파일을 명시적으로 로드하고, 올바른 데이터베이스 URL을 환경 변수에서 읽도록 수정합니다.

### 단계별 해결 과정

#### 1단계: `.env` 파일에 데이터베이스 URL 추가

**목적**: Alembic이 읽을 환경 변수 설정

**작업 내용**:

```ini
DATABASE_URL=postgresql+asyncpg://postgres:ssrinc!123@192.168.164.1:5432/postgres
```

**설명**:
- `postgres+asyncpg://` 스킴: async 드라이버 사용
- `postgres:ssrinc!123`: 사용자명과 비밀번호
- `192.168.164.1:5432`: 원격 PostgreSQL 서버
- `/postgres`: 데이터베이스명

#### 2단계: `backend/alembic/env.py`에서 `.env` 파일 로딩 코드 추가

**목적**: Alembic 시작 시 환경 변수를 명시적으로 로드

**작업 내용**:

```python
from dotenv import load_dotenv
from pathlib import Path
import os

# .env 파일 경로 설정 (alembic/env.py 기준)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
```

**위치**: `env.py` 파일의 맨 위쪽 (import 섹션 이후)

**설명**:
- `Path(__file__).parent.parent`: `alembic/` 디렉토리에서 한 단계 위로 이동 → `backend/` 도착
- `load_dotenv(dotenv_path=env_path)`: 특정 경로의 `.env` 파일 명시적 로드
- 이를 통해 `os.getenv("DATABASE_URL")`이 올바른 값을 반환

#### 3단계: `env.py`에서 환경 변수로부터 DATABASE_URL 읽기

**목적**: 올바른 데이터베이스 URL을 사용하도록 설정

**작업 내용**:

```python
# env.py 내에서 config 설정 부분
config = context.config

# 환경 변수에서 DATABASE_URL 읽기
database_url = os.getenv("DATABASE_URL")

if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
else:
    # 폴백 (필수, 하지만 이제 도달하지 않아야 함)
    config.set_main_option("sqlalchemy.url", "postgresql://localhost/algoref")
```

**설명**:
- 환경 변수가 있으면 우선 사용
- 없는 경우만 폴백 URL 사용 (이제 불필요하지만, 안정성을 위해 유지)

---

## 🧪 검증

### 테스트 방법

```bash
cd backend
alembic upgrade head
```

또는 현재 리비전 상태 확인:

```bash
alembic current
```

### 검증 결과

**기대 결과**:
```
INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO [alembic.runtime.migration] Will assume transactional DDL.
INFO [alembic.migration] Running upgrade () -> 001_initial, create table...
```

**실제 결과**:
```
INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO [alembic.runtime.migration] Will assume transactional DDL.
INFO [alembic.migration] Running upgrade () -> 001, create_user_tables
Current revision(s) for database postgresql+asyncpg://postgres:***@192.168.164.1:5432/postgres: 001
```

### 검증 체크리스트

- [x] 에러 메시지(`WinError 10054`)가 더 이상 발생하지 않음
- [x] `alembic upgrade head` 명령어 성공적으로 실행됨
- [x] 데이터베이스 마이그레이션 정상 적용
- [x] `alembic current`로 현재 리비전 확인 가능
- [x] 원격 PostgreSQL 서버(192.168.164.1:5432)에 올바르게 연결됨

---

## 📝 변경된 파일

### 1. `backend/.env`

**변경 유형**: 추가

**변경 내용**:
- `DATABASE_URL` 환경 변수 추가
- PostgreSQL 연결 정보 포함

**변경 후**:
```ini
DATABASE_URL=postgresql+asyncpg://postgres:ssrinc!123@192.168.164.1:5432/postgres
```

### 2. `backend/alembic/env.py`

**변경 유형**: 수정

**변경 내용**:
- `python-dotenv` import 추가
- `.env` 파일 로딩 로직 추가
- 환경 변수에서 DATABASE_URL 읽기

**변경 전**:
```python
"""The Alembic config object."""
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object
config = context.config
```

**변경 후**:
```python
"""The Alembic config object."""
import os
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# this is the Alembic Config object
config = context.config

# 환경 변수에서 DATABASE_URL 읽기
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
```

---

## 💡 교훈

### 핵심 인사이트

1. **Alembic과 FastAPI의 차이점**
   - FastAPI: `python-dotenv`가 자동으로 `.env` 파일을 로드 (일반적으로)
   - Alembic: 마이그레이션 도구로서 독립적 실행, 명시적 로딩 필요
   - 왜 중요한가: 같은 프로젝트에서도 다른 환경 설정 메커니즘을 요구함

2. **환경 변수 기반 설정의 중요성**
   - 하드코딩된 설정(예: `localhost:5432`)은 개발 환경에만 적합
   - 프로덕션 환경에서는 환경 변수 또는 설정 파일로 관리 필수
   - 왜 중요한가: 보안(자격증명 노출 방지)과 유연성(환경별 설정)

3. **폴백 설정의 위험성**
   - 환경 변수 로딩 실패 시 폴백 값 사용은 디버깅을 어렵게 함
   - 명시적 로딩 확인과 적절한 에러 처리 필요
   - 왜 중요한가: 오류의 진정한 원인(환경 변수 부재)을 파악하기 어려움

### 재발 방지 방안

#### 즉시 적용

- ✅ `.env` 파일에 `DATABASE_URL` 설정
- ✅ Alembic `env.py`에 `python-dotenv` 로딩 코드 추가
- ✅ 모든 팀 멤버에게 이 변경사항 공유

#### 장기 개선

- 📋 개발 환경 설정 가이드 문서 작성 및 유지
- 📋 Alembic 마이그레이션 실행 전 환경 변수 확인 스크립트 작성
- 📋 CI/CD 파이프라인에서 마이그레이션 자동 검증

### 권장사항

#### Do (해야 할 것)

- ✅ 모든 데이터베이스 연결 정보는 환경 변수로 관리
- ✅ 각 환경(개발, 테스트, 프로덕션)에 맞는 `.env` 파일 구성
- ✅ Alembic과 애플리케이션에서 동일한 DATABASE_URL 사용
- ✅ 마이그레이션 실행 후 `alembic current` 명령으로 상태 확인

#### Don't (하지 말아야 할 것)

- ❌ 데이터베이스 연결 정보를 소스 코드에 하드코딩하지 말 것
- ❌ 환경 변수 로딩 실패를 무시하거나 침묵시킬 것
- ❌ 개발과 프로덕션에서 다른 설정 로딩 메커니즘 사용할 것
- ❌ `.env` 파일을 git에 커밋할 것 (`.gitignore`에 추가)

---

## 🔗 관련 이슈

- [FastAPI 환경 변수 설정 가이드]: 애플리케이션과 Alembic의 환경 설정 일관성 확인
- [PostgreSQL 원격 연결 설정]: 원격 서버 연결 시 방화벽 및 네트워크 설정 확인

---

## 📚 참고 자료

### 공식 문서

- [Alembic 공식 문서 - env.py](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-env-py-file)
- [python-dotenv 공식 문서](https://github.com/theskumar/python-dotenv)
- [SQLAlchemy 데이터베이스 연결 문자열](https://docs.sqlalchemy.org/en/20/core/engines.html)
- [asyncpg - PostgreSQL 비동기 드라이버](https://magicstack.github.io/asyncpg/)

### 추가 학습 자료

- 환경 변수 기반 설정 관리의 12 Factor App 원칙
- Alembic을 사용한 데이터베이스 마이그레이션 베스트 프랙티스

---

## 📌 메모

- Windows에서 PostgreSQL 원격 연결 시 방화벽 설정 확인 필요
- 팀원들이 각자의 환경에 맞는 `.env` 파일을 설정해야 함
- `python-dotenv` 패키지가 `requirements.txt`에 포함되어 있는지 확인
- 향후 마이그레이션 자동화 시 환경 변수 검증 단계 추가 고려

---

**작성자**: Claude Code
**마지막 업데이트**: 2025-02-12
