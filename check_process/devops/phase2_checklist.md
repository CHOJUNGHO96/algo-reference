# Phase 2 작업 체크리스트 - DevOps

**작업 기간**: 2024-02-11 완료
**문서 작성일**: 2026-02-12
**담당**: DevOps Specialist

---

## 📋 주요 작업 항목

### 1. Docker 환경 설정 (Priority 1)

#### 1.1 환경 변수 구성
- [x] `.env.example`에서 `.env` 파일 생성
  - [x] 안전한 SECRET_KEY 생성 (32자 랜덤 문자열)
  - [x] Docker 환경용 DATABASE_URL 구성
  - [x] 로컬 개발용 CORS_ORIGINS 설정
  - [x] 프론트엔드용 VITE_API_BASE_URL 추가

**위치**: `D:\workspace_2\algo-reference\.env`

#### 1.2 데이터베이스 마이그레이션 자동화
- [x] `docker-compose.yml` 업데이트하여 마이그레이션 자동 실행
  - [x] 백엔드가 API 서버 시작 전 `alembic upgrade head` 실행
  - [x] 컨테이너 시작 시 데이터베이스 스키마가 항상 최신 상태 유지
  - [x] 우아한 오류 처리 내장

**변경사항**:
```yaml
command: >
  sh -c "alembic upgrade head &&
         uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
```

#### 1.3 Alembic 환경 변수 지원
- [x] `backend/alembic/env.py` 업데이트
  - [x] 환경 변수에서 DATABASE_URL 읽기
  - [x] 환경 변수가 설정되지 않은 경우 alembic.ini로 폴백
  - [x] Docker 컨테이너화된 마이그레이션에 필요

**변경사항**: 18-21번째 줄에 환경 변수 재정의 추가

#### 1.4 Docker 구성 검증
- [x] `docker-compose.yml` 구문 검증 (오류 없음)
- [x] PostgreSQL에 대한 헬스 체크 구성 확인
- [x] 의존성 체인 확인: frontend → backend → postgres
- [x] 개발 hot-reload용 볼륨 마운트 확인

---

### 2. 데이터베이스 백업 시스템 (Priority 2)

데이터베이스 안전을 위한 자동 백업 스크립트 생성:

#### 2.1 Bash 스크립트 (Linux/Mac/Git Bash)
**파일**: `scripts/backup-db.sh`
- [x] 타임스탬프가 포함된 자동 백업
- [x] `backups/` 디렉터리 자동 생성
- [x] Docker 컨테이너에서 pg_dump 사용
- [x] 파일 크기와 함께 성공/실패 보고

**사용법**:
```bash
chmod +x scripts/backup-db.sh
./scripts/backup-db.sh
```

#### 2.2 Windows 배치 스크립트
**파일**: `scripts/backup-db.bat`
- [x] bash 버전과 동일한 기능
- [x] Windows 네이티브 배치 파일
- [x] 색상 코딩된 성공/오류 메시지

**사용법**:
```cmd
scripts\backup-db.bat
```

---

### 3. 검증 및 테스팅 도구 (Priority 3)

#### 3.1 Docker 검증 스크립트 (Bash)
**파일**: `scripts/verify-docker-env.sh`

**기능**:
- [x] 10단계 포괄적 검증 프로세스
- [x] Docker 설치 확인
- [x] .env 파일 검증
- [x] docker-compose.yml 구문 검증
- [x] 포트 충돌 감지
- [x] 자동 빌드 및 시작
- [x] 서비스 헬스 검증
- [x] 데이터베이스 연결 테스트
- [x] 마이그레이션 상태 확인
- [x] 색상 코딩된 출력

#### 3.2 Docker 검증 스크립트 (Windows)
**파일**: `scripts/verify-docker-env.bat`
- [x] Windows 호환 버전
- [x] 동일한 검증 단계
- [x] CMD 친화적 출력

---

### 4. 문서화 (Priority 4)

#### 4.1 Docker 테스팅 가이드
**파일**: `docs/docker-testing-guide.md`

**포괄적 커버리지**:
- [x] 빠른 시작 지침
- [x] 서비스 검증 절차
- [x] 일반 명령어 치트시트
- [x] 문제 해결 가이드
- [x] 테스팅 체크리스트
- [x] 성능 팁
- [x] 모범 사례

**섹션**:
- 사전 요구사항
- 환경 시작
- 서비스 검증
- 일반 명령어 (서비스, 로그, 데이터베이스, 마이그레이션)
- 문제 해결 (8가지 일반적인 이슈 + 수정 방법)
- 테스팅 체크리스트
- 성능 최적화
- 모범 사례

#### 4.2 배포 전략 (기존)
**파일**: `docs/deployment-strategy.md`

이미 포괄적임 (Phase 1에서 생성):
- [x] Railway, Render, Fly.io 배포 가이드
- [x] 환경 변수 구성
- [x] SSL/HTTPS 설정
- [x] 프로덕션 환경의 데이터베이스 마이그레이션
- [x] 모니터링 및 관찰 가능성
- [x] 백업 전략
- [x] 비용 추정
- [x] 보안 체크리스트

---

### 5. CI/CD 파이프라인 검증 (Priority 5)

#### 5.1 GitHub Actions 워크플로우 검토
**파일**: `.github/workflows/ci.yml`

**검증된 구성 포함**:
- [x] PostgreSQL 서비스 컨테이너가 있는 백엔드 테스트
- [x] 커버리지를 포함한 프론트엔드 테스트
- [x] 두 서비스에 대한 Docker 빌드 테스트
- [x] 린팅 (ruff, ESLint)
- [x] 타입 체킹 (mypy, TypeScript)
- [x] Codecov로 커버리지 업로드
- [x] docker-compose 검증

**워크플로우 트리거**:
- `main` 및 `develop` 브랜치로 푸시
- `main`으로의 Pull request

**작업**:
1. `backend-tests`: Python 3.11, pytest, coverage, linting
2. `frontend-tests`: Node 18, npm test, ESLint, TypeScript
3. `docker-build`: 두 Dockerfile에 대한 빌드 검증

#### 5.2 CI/CD 상태
- [x] 워크플로우 구문 유효
- [x] 모든 필요한 단계 존재
- [x] 서비스 의존성 구성됨
- [x] 환경 변수 설정됨
- [x] 커버리지 리포팅 활성화

**참고**: 실제 실행은 GitHub 저장소 설정 및 코드 푸시가 필요합니다.

---

## ✅ 완료 현황

- **총 작업**: 약 35개
- **완료**: 35개 (100%)
- **진행중**: 0개
- **미완료**: 0개

---

## 🔍 검증 항목

### 성공 기준 - 모두 충족 ✅
- [x] `docker-compose up`이 오류 없이 3개 서비스 모두 시작
- [x] 백엔드 http://localhost:8000/docs에서 접근 가능
- [x] 프론트엔드 http://localhost:3000에서 접근 가능
- [x] PostgreSQL 연결 수락 중
- [x] 백엔드 시작 시 데이터베이스 마이그레이션 자동 실행
- [x] 백업 스크립트 작동 (bash 및 batch 모두)
- [x] CI/CD 워크플로우 구문 유효
- [x] 배포 문서화 완료

---

## 📝 비고

### 알려진 이슈 및 참고사항

#### 1. 첫 빌드
- 초기 `docker-compose build`는 5-10분 소요
- 이후 빌드는 캐시 사용 (훨씬 빠름)

#### 2. 프론트엔드 시작 시간
- Vite 개발 서버 시작에 30-60초 소요 가능
- React + TypeScript + hot reload에는 정상적임

#### 3. 포트 충돌
- 5432, 8000, 3000 포트가 사용 가능한지 확인
- 확인 방법: `netstat -an | findstr :<port>` (Windows)

#### 4. 환경 변수
- `.env` 파일은 수동으로 생성해야 함 (git에 커밋되지 않음)
- `.env.example`을 템플릿으로 사용
- 프로덕션용으로 새 SECRET_KEY 생성

#### 5. Windows 경로 처리
- Windows의 Docker는 볼륨과 관련된 경로 문제가 있을 수 있음
- Docker Desktop이 프로젝트 디렉터리에 접근 권한이 있는지 확인
- 더 나은 성능을 위해 WSL2 백엔드 사용

---

### 문제 해결 빠른 참조

#### 백엔드가 시작되지 않음
```bash
docker-compose logs backend
# 일반적인 원인:
# - .env 파일 누락
# - 데이터베이스가 준비되지 않음 (헬스 체크 대기)
# - 마이그레이션 오류
```

#### 프론트엔드가 시작되지 않음
```bash
docker-compose logs frontend
# 일반적인 원인:
# - npm install 실패
# - 포트 3000이 이미 사용 중
# - node_modules 누락 (재빌드: docker-compose up --build -d)
```

#### 데이터베이스 연결 오류
```bash
# PostgreSQL이 정상인지 확인
docker-compose ps postgres

# 연결 테스트
docker-compose exec postgres pg_isready -U algoref_user

# DATABASE_URL 형식 확인
echo $DATABASE_URL  # 다음과 같아야 함: postgresql+asyncpg://user:pass@host:5432/db
```

#### 마이그레이션 실패
```bash
# 현재 상태 확인
docker-compose exec backend alembic current

# 수동 마이그레이션
docker-compose exec backend alembic upgrade head

# 데이터베이스 리셋 (경고: 데이터 삭제)
docker-compose down -v
docker-compose up -d
```

---

## 🚀 Docker 환경 실행 방법

### 빠른 테스트 스위트

```bash
# 1. docker-compose 검증
docker-compose config

# 2. 이미지 빌드
docker-compose build

# 3. 서비스 시작
docker-compose up -d

# 4. 상태 확인 (모두 "Up"이어야 함)
docker-compose ps

# 5. 백엔드 검증
curl http://localhost:8000/docs

# 6. 프론트엔드 검증
curl http://localhost:3000

# 7. 데이터베이스 테스트
docker-compose exec postgres psql -U algoref_user -d algoref -c "SELECT 1;"

# 8. 마이그레이션 확인
docker-compose exec backend alembic current

# 9. 로그 보기
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# 10. 서비스 중지
docker-compose down
```

### 자동화된 검증

**Linux/Mac/Git Bash**:
```bash
chmod +x scripts/verify-docker-env.sh
./scripts/verify-docker-env.sh
```

**Windows**:
```cmd
scripts\verify-docker-env.bat
```

---

## 📂 생성/수정된 파일

### 새로 생성된 파일
1. `.env` - 환경 변수 (커밋되지 않음)
2. `scripts/backup-db.sh` - 데이터베이스 백업 (Bash)
3. `scripts/backup-db.bat` - 데이터베이스 백업 (Windows)
4. `scripts/verify-docker-env.sh` - 환경 검증 (Bash)
5. `scripts/verify-docker-env.bat` - 환경 검증 (Windows)
6. `docs/docker-testing-guide.md` - 테스팅 문서화
7. `DEVOPS_PHASE2_COMPLETE.md` - 영문 완료 보고서

### 수정된 파일
1. `docker-compose.yml` - 마이그레이션 자동화 추가
2. `backend/alembic/env.py` - 환경 변수 지원 추가

---

## 🎯 권장 사항

### 개발 팀을 위한 권장사항
1. **매일 작업 시작 전 검증 스크립트 실행**
2. **문제 발생 시 로그 자주 확인**
3. **주요 스키마 변경 전 데이터베이스 백업**
4. **새로 시작하려면 클린 슬레이트 사용** (`docker-compose down -v`)
5. **.env를 .env.example과 동기화 유지** (변수 추가 시 템플릿 업데이트)

### 프로덕션 배포를 위한 권장사항
1. **새 SECRET_KEY 생성** (개발 키 절대 사용 금지)
2. **관리형 PostgreSQL 사용** (Railway/Supabase) 백업용
3. **모니터링 활성화** (Sentry, Datadog 등)
4. **플랫폼 기본값 이상의 자동 백업 설정**
5. **배포 전 마이그레이션 롤백 절차 테스트**

### CI/CD를 위한 권장사항
1. **GitHub에 시크릿 추가** (Codecov 토큰, 배포 키)
2. **main 브랜치 보호 활성화** (CI 통과 필요)
3. **브랜치에 푸시하여 워크플로우 테스트**
4. **파이프라인 실패 모니터링**
5. **CI에서 배포 설정** (향후: 스테이징 자동 배포)

---

## 🎉 결론

Docker 환경이 완전히 구성되고 검증되었습니다. 모든 Phase 2 DevOps 목표 완료:

- ✅ 자동 마이그레이션이 있는 Docker Compose 설정
- ✅ 안전한 기본값을 갖춘 환경 구성
- ✅ 크로스 플랫폼 데이터베이스 백업 시스템
- ✅ 포괄적인 검증 도구
- ✅ CI/CD 파이프라인 검증 완료
- ✅ 완전한 문서화

**상태**: 백엔드 CRUD (Task #12) 및 프론트엔드 API 통합 (Task #13)과의 통합 준비 완료

---

## 🔗 리소스

### 문서
- [Docker Testing Guide](docs/docker-testing-guide.md)
- [Deployment Strategy](docs/deployment-strategy.md)
- [Docker README](DOCKER_README.md)

### 스크립트
- `scripts/backup-db.sh` - 데이터베이스 백업 (Bash)
- `scripts/backup-db.bat` - 데이터베이스 백업 (Windows)
- `scripts/verify-docker-env.sh` - 전체 검증 (Bash)
- `scripts/verify-docker-env.bat` - 전체 검증 (Windows)

### 주요 파일
- `docker-compose.yml` - 서비스 오케스트레이션
- `.env.example` - 환경 변수 템플릿
- `.github/workflows/ci.yml` - CI/CD 파이프라인

---

## 🔄 다음 단계

### 즉시 (Phase 2)
1. ✅ Docker 환경 테스트 및 작동
2. ⏳ 백엔드 CRUD 구현 (Task #12 - 진행 중)
3. ⏳ 프론트엔드 API 통합 (Task #13 - 진행 중)
4. ⏳ AI 콘텐츠 생성 (Task #14 - 진행 중)
5. ⏳ 통합 테스트 (Task #16 - 대기 중)

### 향후 (Phase 3 - 프로덕션)
1. Railway/Render 스테이징 환경에 배포
2. 프로덕션 환경 변수 구성
3. 모니터링 설정 (Sentry)
4. 프로덕션 데이터베이스에서 자동 백업 활성화
5. 커스텀 도메인 및 SSL 구성
6. 부하 테스트 및 성능 최적화
7. 보안 감사

---

**작성자**: DevOps Phase 2 구현 팀
**참조 문서**: `DEVOPS_PHASE2_COMPLETE.md`
