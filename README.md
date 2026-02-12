# 알고리즘 참고 자료 (Algorithm Reference)

문제 풀이가 아닌 공식/패턴 중심으로 알고리즘을 정리하는 코딩 테스트 대비 참고 플랫폼입니다.

## 🎯 프로젝트 비전

**타겟 사용자**: 암기식 학습에서 구조적 이해로 전환하고 싶은 코딩 테스트 준비 초중급 개발자

**핵심 가치**: 단순 문제 풀이가 아닌 '공식 + 사고 과정 + 적용 패턴 + 코드 템플릿'을 체계화한 참고 사이트

## 🏗️ 아키텍처

### 기술 스택

**Backend**:
- FastAPI (Python 3.11+) - 모던 비동기 웹 프레임워크
- PostgreSQL 15+ - 전문 검색 기능 포함 프로덕션 데이터베이스
- SQLAlchemy 2.0 - 비동기 ORM
- Pydantic v2 - 데이터 검증
- JWT 인증 - 관리자 보안

**Frontend**:
- React 18 + TypeScript - 모던 UI 프레임워크
- Vite - 초고속 빌드 도구
- Redux Toolkit + RTK Query - 상태 관리 + API
- Ant Design - 전문 UI 컴포넌트
- Prism.js - 코드 구문 강조

**DevOps**:
- Docker + Docker Compose - 로컬 개발 환경
- GitHub Actions - CI/CD
- Pytest + Jest - 테스팅
- Playwright - E2E 테스팅

### 데이터베이스 스키마

**핵심 테이블**:
- `categories` - 알고리즘 카테고리 (투 포인터, 슬라이딩 윈도우, DP 등)
- `difficulty_levels` - 난이도 (쉬움, 보통, 어려움)
- `programming_languages` - 프로그래밍 언어 (Python, C++, Java)
- `algorithms` - 메인 콘텐츠 (8가지 구조)
- `code_templates` - 언어별 코드 템플릿
- `users` - 관리자 인증

### API 구조

**공개 엔드포인트**:
- `GET /api/v1/algorithms` - 필터링 포함 목록 조회
- `GET /api/v1/algorithms/{slug}` - 상세 조회
- `GET /api/v1/categories` - 카테고리 트리
- `GET /api/v1/languages` - 지원 언어 목록

**관리자 엔드포인트** (JWT 인증):
- `POST /api/v1/auth/login` - 관리자 로그인
- `POST /api/v1/admin/algorithms` - 생성
- `PUT /api/v1/admin/algorithms/{id}` - 수정
- `DELETE /api/v1/admin/algorithms/{id}` - 삭제

전체 OpenAPI 명세는 `api-contract.yaml` 파일을 참고하세요.

## 📐 8가지 콘텐츠 구조

각 알고리즘은 다음 체계적인 구조를 따릅니다:

1. **개념 요약** - 한 문단 설명
2. **핵심 공식/패턴** - 구문 강조된 핵심 공식
3. **사고 과정** - 단계별 접근 방법
4. **적용 조건** - 언제 사용 / 언제 사용하지 말아야 하는지
5. **시간/공간 복잡도** - 하이라이트 박스로 표시된 Big-O 표기법
6. **대표 문제 유형** - 일반적인 문제 패턴
7. **코드 템플릿** - Python, C++, Java 탭과 복사 버튼
8. **주의사항** - 흔한 실수 경고

## 🎨 디자인 철학

**시각적 아이덴티티**:
- 기본 테마: 다크 모드 (GitHub Dark: #0d1117 배경, #e6edf3 텍스트)
- 라이트 모드 토글 가능
- 카테고리별 색상 코드 (파랑: 투 포인터, 보라: 슬라이딩 윈도우 등)
- 모던하고 개발자 친화적인 디자인

**레이아웃 패턴**:
```
데스크톱 (3단 레이아웃):
┌──────────────┬─────────────────────────────┬──────────┐
│ 사이드바     │  알고리즘 카드 그리드 (3-4) │ 상세정보 │
│ (240px)      │                             │ 사이드바 │
│              │  [카드] [카드] [카드]       │ (280px)  │
│ - 카테고리   │  [카드] [카드] [카드]       │          │
│ - 검색       │                             │          │
│ - 필터       │  페이지네이션               │          │
└──────────────┴─────────────────────────────┴──────────┘
```

## 🚀 빠른 시작

### 사전 요구사항
- Docker & Docker Compose
- Node.js 18+ (로컬 프론트엔드 개발용)
- Python 3.11+ (로컬 백엔드 개발용)

### 로컬 개발 환경 설정

1. **클론 및 설정**:
```bash
git clone https://github.com/CHOJUNGHO96/algo-reference.git
cd algo-reference
cp .env.example .env  # 설정 업데이트
```

2. **Docker Compose로 서비스 시작**:
```bash
docker-compose up -d
```

3. **데이터베이스 마이그레이션 실행**:
```bash
docker-compose exec backend alembic upgrade head
```

4. **초기 데이터 시드**:
```bash
docker-compose exec backend python scripts/seed_data.py
```

5. **애플리케이션 접속**:
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 개발 워크플로우

**백엔드 개발**:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**프론트엔드 개발**:
```bash
cd frontend
npm install
npm run dev
```

**테스트 실행**:
```bash
# 백엔드 테스트
cd backend
pytest --cov=app

# 프론트엔드 테스트
cd frontend
npm test

# E2E 테스트
cd tests/e2e
npx playwright test
```

## 👥 팀 구조

이 프로젝트는 명확한 소유권을 가진 병렬 팀 접근 방식으로 구축됩니다:

| 역할 | 담당 영역 | 주요 책임 |
|------|-----------|----------|
| **백엔드 아키텍트** | `backend/` | FastAPI, SQLAlchemy, API 엔드포인트, JWT 인증 |
| **프론트엔드 아키텍트** | `frontend/` | React, TypeScript, Redux, UI 컴포넌트 |
| **콘텐츠 생성기** | `content-generator/` | AI 생성 알고리즘 콘텐츠, 검증 |
| **DevOps 전문가** | Docker, CI/CD | 인프라, 배포, 모니터링 |
| **QA 전문가** | `tests/` | 테스팅 전략, pytest, Jest, Playwright |
| **팀 리드** | 조율 | API 계약, 통합, 배포 |

## 📊 개발 단계

### 1단계: 기반 구축 (현재 - 3시간)
- ✅ API 계약 명세 (OpenAPI)
- 🔄 백엔드 프로젝트 구조
- 🔄 프론트엔드 프로젝트 구조
- 🔄 콘텐츠 생성 준비
- 🔄 Docker 개발 환경
- 🔄 테스팅 인프라

### 2단계: 핵심 구현 (5시간)
- 백엔드 CRUD 엔드포인트
- 프론트엔드 알고리즘 목록 & 상세 페이지
- 관리자 CMS 인터페이스
- AI 생성 콘텐츠 (15-20개 알고리즘)
- 데이터베이스 시딩
- 통합 테스트

### 3단계: 통합 & 배포 (4시간)
- E2E 테스팅
- 성능 최적화
- 접근성 개선
- 프로덕션 배포
- 모니터링 설정
- 최종 QA

## 📝 콘텐츠 생성

알고리즘은 다음을 보장하기 위해 구조화된 프롬프트를 사용하여 AI로 생성됩니다:
- 모든 항목의 일관성
- 정확한 코드 템플릿
- 실제 LeetCode 문제 참조
- 흔한 실수 식별

목표: 다음을 다루는 15-20개 핵심 알고리즘:
- 투 포인터 패턴
- 슬라이딩 윈도우 기법
- 이진 탐색 변형
- DFS/BFS 순회
- 동적 프로그래밍 (1D/2D)
- 그리디 알고리즘
- Union-Find
- 위상 정렬
- 그 외 다수...

## 🧪 테스팅 전략

**커버리지 목표**:
- 백엔드 단위 테스트: ≥80%
- 프론트엔드 단위 테스트: ≥75%
- 통합 테스트: ≥75% 엔드포인트
- E2E 테스트: 100% 핵심 플로우

**품질 게이트**:
- 병합 전 모든 테스트 통과 필수
- 프로덕션 빌드에서 콘솔 에러 없음
- API 응답 시간 p95 <200ms
- 프론트엔드 LCP <2s
- Lighthouse 점수 ≥90

## 🚀 배포

**백엔드**: Railway / Render / Fly.io
**프론트엔드**: Vercel / Netlify
**데이터베이스**: Railway PostgreSQL / Supabase
**모니터링**: Sentry (에러 추적)

## 📖 API 문서

인터랙티브 API 문서:
- 개발: http://localhost:8000/docs
- 프로덕션: https://api.algoref.com/docs

## 🤝 기여하기

이 프로젝트는 프로덕션 데모 프로젝트입니다. 기여를 원하신다면:

1. API 계약 검토 (`api-contract.yaml`)
2. 8가지 콘텐츠 구조 확인
3. 기존 코드 패턴 따르기
4. 테스트 통과 및 커버리지 유지 확인
5. 문서 업데이트

## 📜 라이선스

MIT License - 자세한 내용은 LICENSE 파일 참조

## 🎓 학습 리소스

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [React 문서](https://react.dev/)
- [PostgreSQL 전문 검색](https://www.postgresql.org/docs/current/textsearch.html)
- [TypeScript 핸드북](https://www.typescriptlang.org/docs/)

---

**기술 스택**: FastAPI, React, TypeScript, PostgreSQL, Docker

**목적**: 알고리즘 학습 플랫폼을 위한 풀스택 개발 모범 사례 시연

**GitHub**: https://github.com/CHOJUNGHO96/algo-reference
