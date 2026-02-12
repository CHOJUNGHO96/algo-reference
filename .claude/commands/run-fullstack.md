# 전체 스택 실행

Backend + Frontend + PostgreSQL을 Docker Compose로 실행합니다.

## 사용법

```
/run-fullstack [모드]
```

## 예시

```bash
# Docker Compose로 전체 스택 실행
/run-fullstack

# 개발 모드 (로컬 실행)
/run-fullstack dev

# 로그 확인
/run-fullstack logs

# 종료
/run-fullstack stop
```

## 실행 과정

### Docker Compose 모드 (기본)

1. `docker-compose.yml` 파일 확인
2. 모든 컨테이너 빌드 및 실행:
   - PostgreSQL (포트 5432)
   - Backend (포트 8000)
   - Frontend (포트 3000)
3. 로그 스트리밍

### 개발 모드 (로컬)

1. **Backend**: uvicorn 개발 서버 실행 (hot reload)
2. **Frontend**: Vite 개발 서버 실행 (hot reload)
3. **PostgreSQL**: 별도 실행 필요

## 명령어

```bash
# Docker Compose 실행 (detached mode)
docker-compose up -d

# 로그 확인 (follow mode)
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f backend

# 전체 종료
docker-compose down

# 볼륨까지 삭제
docker-compose down -v
```

### 개발 모드 명령어

```bash
# Backend (터미널 1)
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (터미널 2)
cd frontend
npm run dev
```

## 접속 URL

- **Backend API**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432

## 상태 확인

```bash
# 컨테이너 상태 확인
docker-compose ps

# 헬스 체크
curl http://localhost:8000/health
curl http://localhost:3000
```

## 트러블슈팅

### 포트 이미 사용 중

```bash
# 포트 사용 확인
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 프로세스 종료 (Windows)
taskkill /PID <PID> /F
```

### 컨테이너 재시작

```bash
# 특정 서비스만 재시작
docker-compose restart backend

# 전체 재시작
docker-compose restart
```

## 관련 명령어

- `/test-backend`: Backend 테스트
- `/test-frontend`: Frontend 테스트
- `/migration-create`: DB 마이그레이션
