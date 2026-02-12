# Claude Code 사용 가이드

이 문서는 Algo Reference 프로젝트에서 Claude Code를 효과적으로 사용하는 방법을 안내합니다.

**생성일**: 2026-02-12
**대상**: 프로젝트 개발자 전체
**난이도**: 초급~중급

---

## 📑 목차

1. [시작하기](#시작하기)
2. [Commands 사용법](#commands-사용법)
3. [Agents 사용법](#agents-사용법)
4. [Skills 활용법](#skills-활용법)
5. [Settings 커스터마이징](#settings-커스터마이징)
6. [실전 워크플로우](#실전-워크플로우)
7. [트러블슈팅](#트러블슈팅)
8. [FAQ](#faq)

---

## 시작하기

### 프로젝트 구조 확인

```
algo-reference/
├── CLAUDE.md                    # 개발 가이드 (필수 읽기!)
├── .claude/
│   ├── settings.json           # 전역 설정
│   ├── settings.local.json     # 로컬 설정 (훅, 권한)
│   ├── commands/               # 5개의 커스텀 명령어
│   ├── agents/                 # 5개의 전문 에이전트
│   └── skills/                 # 8개의 프로젝트 스킬
└── docs/
    └── CLAUDE_CODE_USAGE_GUIDE.md  # 이 문서
```

### 필수 확인 사항

✅ **CLAUDE.md 읽기**: 프로젝트 코딩 컨벤션, 워크플로우 확인
✅ **Python venv 활성화**: Backend 작업 시 `.venv` 활성화
✅ **Node.js 설치**: Frontend 작업 시 `npm` 사용 가능 확인

---

## Commands 사용법

Commands는 자주 사용하는 작업을 슬래시 명령어로 실행할 수 있게 해줍니다.

### 사용 가능한 Commands

| Command | 설명 | 예시 |
|---------|------|------|
| `/test-backend` | Backend pytest 테스트 실행 | `/test-backend tests/test_users.py` |
| `/test-frontend` | Frontend vitest 테스트 실행 | `/test-frontend run` |
| `/migration-create` | Alembic 마이그레이션 생성 | `/migration-create "add user email"` |
| `/run-fullstack` | 전체 스택 실행 (Docker) | `/run-fullstack` |
| `/lint-fix` | 린트 자동 수정 | `/lint-fix backend` |

### 1. Backend 테스트 실행

#### 전체 테스트

```
/test-backend
```

**실행 내용**:
```bash
cd backend && pytest tests/ -v --tb=short
```

#### 특정 파일 테스트

```
/test-backend tests/test_users.py
```

#### 커버리지 포함

```
/test-backend --coverage
```

**결과 확인**:
- 터미널에 테스트 결과 출력
- `backend/htmlcov/index.html`에 HTML 리포트 생성

### 2. Frontend 테스트 실행

#### Watch 모드 (개발 중)

```
/test-frontend
```

**실행 내용**:
```bash
cd frontend && npm run test
```

#### 1회 실행 (CI/CD)

```
/test-frontend run
```

#### 커버리지 확인

```
/test-frontend coverage
```

#### UI 모드 (시각적 테스트)

```
/test-frontend ui
```

**브라우저**: http://localhost:51204 (Vitest UI)

### 3. 데이터베이스 마이그레이션

#### 새 마이그레이션 생성

```
/migration-create "add user email field"
```

**실행 내용**:
```bash
cd backend && alembic revision --autogenerate -m "add user email field"
```

**생성 위치**: `backend/alembic/versions/xxxx_add_user_email_field.py`

#### 마이그레이션 적용

```
/migration-create apply
```

**실행 내용**:
```bash
cd backend && alembic upgrade head
```

#### 현재 리비전 확인

```
/migration-create current
```

#### 히스토리 확인

```
/migration-create history
```

### 4. 전체 스택 실행

#### Docker Compose로 실행

```
/run-fullstack
```

**실행 내용**:
```bash
docker-compose up -d
docker-compose logs -f
```

**접속 URL**:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Swagger UI: http://localhost:8000/docs

#### 개발 모드 (로컬 실행)

```
/run-fullstack dev
```

**2개의 터미널 실행**:
1. Backend: `uvicorn app.main:app --reload`
2. Frontend: `npm run dev`

#### 로그 확인

```
/run-fullstack logs
```

#### 종료

```
/run-fullstack stop
```

### 5. 린트 자동 수정

#### Backend 포맷팅

```
/lint-fix backend
```

**실행 내용**:
```bash
cd backend && black app/ tests/
cd backend && isort app/ tests/
```

#### Frontend 린트 수정

```
/lint-fix frontend
```

**실행 내용**:
```bash
cd frontend && npm run lint -- --fix
cd frontend && npx prettier --write "src/**/*.{ts,tsx}"
```

#### 전체 수정

```
/lint-fix all
```

---

## Agents 사용법

Agents는 전문화된 작업을 자동으로 수행하는 AI 에이전트입니다.

### 사용 가능한 Agents

| Agent | 설명 | 주요 기능 |
|-------|------|----------|
| `backend-reviewer` | Backend 코드 리뷰 | 타입 힌트, 보안, 성능 검사 |
| `frontend-reviewer` | Frontend 코드 리뷰 | TypeScript, React 패턴, 접근성 |
| `test-runner` | 테스트 실행 및 분석 | 실패 분석, Coverage 리포트 |
| `api-doc-generator` | API 문서 생성 | OpenAPI 스펙, 코드 예시 |
| `troubleshooting-historian` | 이슈 해결 기록 | 트러블슈팅 문서화 |

### Agent 실행 방법

#### 기본 문법

```
/agents run <agent-name> <arguments>
```

또는 대화형으로:

```
@<agent-name> <작업 설명>
```

### 1. Backend 코드 리뷰

#### 특정 파일 리뷰

```
/agents run backend-reviewer backend/app/api/routes/users.py
```

또는:

```
@backend-reviewer 이 파일을 리뷰해줘: backend/app/api/routes/users.py
```

**리뷰 항목**:
- ✅ Type hints 완전성
- ✅ Docstring 존재 여부
- ✅ 비동기 함수 사용 (`async def`)
- ✅ SQL Injection 방지
- ✅ 에러 처리 적절성
- ✅ 성능 최적화 기회

**출력 예시**:

```markdown
## 리뷰 결과: backend/app/api/routes/users.py

### ✅ 잘된 점
- 비동기 함수 사용
- Pydantic 스키마 검증

### ⚠️ 개선 필요 (High Priority)

#### 1. Type hints 누락
**위치**: Line 25
**개선**:
```python
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    ...
```

### 📊 통계
- Type hints 커버리지: 60% (권장: 100%)
- 보안 이슈: 2개
```

#### 여러 파일 리뷰

```
@backend-reviewer backend/app/api/routes/ 폴더의 모든 파일을 리뷰해줘
```

### 2. Frontend 코드 리뷰

#### React 컴포넌트 리뷰

```
/agents run frontend-reviewer frontend/src/components/UserForm.tsx
```

**리뷰 항목**:
- ✅ TypeScript 타입 정의
- ✅ `any` 타입 사용 금지
- ✅ React Hooks 올바른 사용
- ✅ 접근성 (a11y)
- ✅ 성능 최적화 (useMemo, useCallback)
- ✅ 에러 처리

**출력 예시**:

```markdown
## 리뷰 결과: frontend/src/components/UserForm.tsx

### ⚠️ 개선 필요

#### 1. `any` 타입 사용
**위치**: Line 15
**개선**:
```typescript
type FormData = z.infer<typeof userSchema>;
const handleSubmit = (data: FormData) => { ... }
```

#### 2. 접근성 - label 누락
**위치**: Line 28
**개선**:
```tsx
<label htmlFor="email">Email</label>
<input id="email" {...register('email')} aria-label="Email address" />
```
```

### 3. 테스트 실행 및 분석

#### Backend 테스트 분석

```
/agents run test-runner --backend
```

**수행 작업**:
1. pytest 실행
2. 실패한 테스트 분석
3. 에러 원인 파악
4. 수정 방안 제시
5. Coverage 리포트 생성

**출력 예시**:

```markdown
## 테스트 결과 분석

### 📊 요약
- 전체: 25개
- 통과: 23개 ✅
- 실패: 2개 ❌
- Coverage: 87%

### ❌ 실패한 테스트

#### test_create_user_with_invalid_email
**원인**: Pydantic validation이 422를 반환하지만 테스트는 400을 기대
**수정**:
```python
assert response.status_code == 422  # 400 → 422
```
```

#### Frontend 테스트 분석

```
/agents run test-runner --frontend
```

### 4. API 문서 생성

#### 전체 API 문서 생성

```
/agents run api-doc-generator
```

**생성 파일**:
- `docs/api/README.md`: API 개요
- `docs/api/users.md`: Users API 상세
- `docs/api/auth.md`: Auth API 상세
- `api-contract.json`: OpenAPI 스펙

**출력 예시**:

```markdown
# Users API

## POST /api/v1/users

### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### Response (200 OK)
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-02-12T10:30:00Z"
}
```

### Code Examples

**Python**:
```python
response = await client.post("/api/v1/users", json=data)
```

**JavaScript**:
```javascript
const response = await axios.post('/api/v1/users', data);
```
```

#### 특정 라우터만 문서화

```
/agents run api-doc-generator --router users
```

### 5. 트러블슈팅 기록

#### 해결한 이슈 문서화

```
@troubleshooting-historian 방금 해결한 데이터베이스 연결 오류를 문서화해줘
```

**생성 위치**: `issue/database/YYYY-MM-DD-issue-name.md`

**문서 내용**:
- 문제 상황
- 에러 메시지
- 원인 분석
- 해결 방법
- 검증 결과
- 교훈 및 권장사항

---

## Skills 활용법

Skills는 프로젝트 컨텍스트를 Claude에게 제공하여 더 정확한 응답을 가능하게 합니다.

### 사용 가능한 Skills

#### 공통 Skills

| Skill | 설명 | 자동 활성화 조건 |
|-------|------|-----------------|
| `algo-reference-architecture` | 프로젝트 구조, 아키텍처 패턴 | 폴더 구조, 의존성 질문 |
| `algo-reference-testing` | 테스트 작성 패턴 | 테스트 코드 작성 시 |

#### Backend Skills

| Skill | 설명 | 자동 활성화 조건 |
|-------|------|-----------------|
| `algo-reference-api` | FastAPI 라우터 패턴 | `api/routes/` 파일 작업 시 |
| `algo-reference-models` | SQLAlchemy 모델, Pydantic 스키마 | `models/`, `schemas/` 작업 시 |
| `algo-reference-database` | DB 연결, Alembic 마이그레이션 | DB 관련 질문, 마이그레이션 작업 시 |

#### Frontend Skills

| Skill | 설명 | 자동 활성화 조건 |
|-------|------|-----------------|
| `algo-reference-components` | React 컴포넌트, Ant Design | `components/` 작업 시 |
| `algo-reference-state` | Redux Toolkit 상태 관리 | `store/` 작업 시 |
| `algo-reference-forms` | React Hook Form + Zod | 폼 처리 코드 작성 시 |

### Skills 자동 활성화

Skills는 **자동으로 활성화**되므로 별도 명령어가 필요 없습니다!

#### 예시 1: API 엔드포인트 작성

**질문**:
```
/api/v1/users 엔드포인트에 사용자 목록 조회 기능을 추가해줘
```

**자동 활성화**: `algo-reference-api`, `algo-reference-models`

**Claude 응답**:
```python
# algo-reference-api 스킬에 따라 FastAPI 패턴 적용
@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[UserResponse]:
    """사용자 목록 조회"""
    result = await db.execute(
        select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
    )
    return result.scalars().all()
```

#### 예시 2: React 컴포넌트 작성

**질문**:
```
사용자 프로필을 표시하는 UserCard 컴포넌트를 만들어줘
```

**자동 활성화**: `algo-reference-components`

**Claude 응답**:
```typescript
// algo-reference-components 스킬에 따라 Ant Design 활용
import { FC } from 'react';
import { Card, Avatar } from 'antd';

type UserCardProps = {
  user: User;
  onClick?: () => void;
};

export const UserCard: FC<UserCardProps> = ({ user, onClick }) => {
  return (
    <Card hoverable onClick={onClick}>
      <Card.Meta
        avatar={<Avatar>{user.fullName[0]}</Avatar>}
        title={user.fullName}
        description={user.email}
      />
    </Card>
  );
};
```

#### 예시 3: 폼 검증

**질문**:
```
회원가입 폼에 비밀번호 강도 검증을 추가해줘
```

**자동 활성화**: `algo-reference-forms`

**Claude 응답**:
```typescript
// algo-reference-forms 스킬에 따라 Zod validation 적용
const signupSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  password: z
    .string()
    .min(8, '비밀번호는 최소 8자입니다')
    .regex(/[A-Z]/, '최소 1개의 대문자가 필요합니다')
    .regex(/[0-9]/, '최소 1개의 숫자가 필요합니다'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: '비밀번호가 일치하지 않습니다',
  path: ['confirmPassword']
});
```

### Skills 수동 참조

필요 시 특정 스킬을 명시적으로 참조할 수 있습니다:

```
@algo-reference-database 마이그레이션 충돌을 어떻게 해결하나요?
```

---

## Settings 커스터마이징

### settings.local.json 구조

```json
{
  "hooks": {
    "PostToolUse": [...],  // 도구 사용 후 실행
    "PreCommit": [...]     // 커밋 전 실행
  },
  "permissions": {
    "allow": [...],        // 자동 승인 명령어
    "deny": [...],         // 차단 명령어
    "ask": [...]           // 사용자 확인 명령어
  }
}
```

### 1. Hooks 커스터마이징

#### PostToolUse Hook 수정

**현재 설정**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "cd frontend && npx prettier --write {file} || true",
            "description": "프론트엔드 코드 자동 포맷팅"
          }
        ]
      }
    ]
  }
}
```

**Backend 포맷팅 추가**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "cd frontend && npx prettier --write {file} || true",
            "description": "Frontend 자동 포맷팅"
          },
          {
            "type": "command",
            "command": "cd backend && black {file} || true",
            "description": "Backend 자동 포맷팅"
          }
        ]
      }
    ]
  }
}
```

#### PreCommit Hook 수정

**타입 체크 추가**:
```json
{
  "hooks": {
    "PreCommit": [
      {
        "type": "command",
        "command": "cd backend && pytest tests/ -v --tb=short || echo 'Tests failed'",
        "description": "Backend 테스트"
      },
      {
        "type": "command",
        "command": "cd frontend && npm run build || echo 'Build failed'",
        "description": "Frontend 타입 체크"
      }
    ]
  }
}
```

### 2. Permissions 커스터마이징

#### 위험한 명령어 차단

**추가 차단 명령어**:
```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(pip install * --global)",
      "Bash(npm install -g *)",      // 추가
      "Bash(chmod 777 *)",            // 추가
      "Bash(chown *)"                 // 추가
    ]
  }
}
```

#### 자동 승인 명령어 추가

**빌드 명령어 자동 승인**:
```json
{
  "permissions": {
    "allow": [
      "Bash(cd backend && pytest *)",
      "Bash(cd backend && alembic *)",
      "Bash(cd frontend && npm run *)",
      "Bash(cd frontend && npm test *)",
      "Bash(npm run build)",          // 추가
      "Bash(npm run lint)",            // 추가
      "Bash(docker-compose up *)"      // 추가
    ]
  }
}
```

#### 확인 필요 명령어 추가

**프로덕션 배포 확인**:
```json
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(git commit *)",
      "Bash(alembic downgrade *)",
      "Bash(npm publish *)",           // 추가
      "Bash(docker push *)",           // 추가
      "Bash(kubectl apply *)"          // 추가
    ]
  }
}
```

### 3. 팀별 설정 공유

`.claude/settings.local.json`을 Git에 커밋하여 팀 전체가 동일한 설정을 사용할 수 있습니다.

```bash
# .gitignore에서 제거
# .claude/settings.local.json  # 주석 처리 또는 삭제

# Git에 추가
git add .claude/settings.local.json
git commit -m "Add Claude Code team settings"
```

---

## 실전 워크플로우

### 시나리오 1: 새 API 엔드포인트 추가

#### 1단계: 요구사항 정의

```
게시글 CRUD API를 만들어줘. 다음 기능이 필요해:
- 게시글 목록 조회 (페이지네이션)
- 게시글 상세 조회
- 게시글 작성 (로그인 필요)
- 게시글 수정 (작성자만)
- 게시글 삭제 (작성자 또는 관리자)
```

**Claude 응답**: `algo-reference-architecture`, `algo-reference-api`, `algo-reference-models` 스킬 자동 활성화

#### 2단계: 모델 생성

Claude가 다음 파일들을 생성:
- `backend/app/models/post.py`
- `backend/app/schemas/post.py`

#### 3단계: 마이그레이션 생성

```
/migration-create "add post table"
```

#### 4단계: API 라우터 작성

Claude가 생성:
- `backend/app/api/routes/posts.py`

#### 5단계: 라우터 등록

Claude가 `backend/app/main.py`에 라우터 추가

#### 6단계: 테스트 작성

```
posts.py에 대한 테스트 코드를 작성해줘
```

Claude가 생성:
- `backend/tests/test_posts.py`

#### 7단계: 테스트 실행

```
/test-backend tests/test_posts.py
```

#### 8단계: 코드 리뷰

```
/agents run backend-reviewer backend/app/api/routes/posts.py
```

#### 9단계: API 문서 생성

```
/agents run api-doc-generator --router posts
```

### 시나리오 2: React 컴포넌트 개발

#### 1단계: 컴포넌트 요구사항

```
게시글 목록을 표시하는 PostList 컴포넌트를 만들어줘.
- Ant Design Table 사용
- 페이지네이션
- 검색 기능
- 작성일 정렬
```

**Claude 응답**: `algo-reference-components` 스킬 자동 활성화

#### 2단계: 상태 관리 추가

```
게시글 데이터를 Redux로 관리하도록 수정해줘
```

**Claude 응답**: `algo-reference-state` 스킬 자동 활성화
- `frontend/src/store/postSlice.ts` 생성

#### 3단계: API 통신 추가

```
Redux Thunk로 게시글 목록을 가져오는 기능을 추가해줘
```

#### 4단계: 테스트 작성

```
PostList 컴포넌트에 대한 테스트를 작성해줘
```

**Claude 응답**: `algo-reference-testing` 스킬 자동 활성화
- `frontend/src/components/PostList.test.tsx` 생성

#### 5단계: 테스트 실행

```
/test-frontend src/components/PostList.test.tsx
```

#### 6단계: 코드 리뷰

```
/agents run frontend-reviewer frontend/src/components/PostList.tsx
```

### 시나리오 3: 버그 수정 및 문서화

#### 1단계: 버그 발견

```
게시글 삭제 시 404 에러가 발생해. 원인을 찾아줘.
```

#### 2단계: 테스트 실행 및 분석

```
/agents run test-runner --backend tests/test_posts.py
```

**Agent 분석**:
- 실패한 테스트 식별
- 에러 메시지 해석
- 원인 파악
- 수정 방안 제시

#### 3단계: 수정

```
제안한 수정 사항을 적용해줘
```

#### 4단계: 재테스트

```
/test-backend tests/test_posts.py::test_delete_post
```

#### 5단계: 이슈 문서화

```
@troubleshooting-historian 방금 해결한 게시글 삭제 404 에러를 문서화해줘
```

**생성 위치**: `issue/api/20260212_post_delete_404_error.md`

#### 6단계: 커밋

```
변경사항을 커밋해줘
```

**PreCommit Hook 실행**:
- Backend 테스트 실행
- Frontend 린트 체크

**Claude가 커밋 메시지 생성**:
```
fix(api): resolve 404 error when deleting posts

- Fix endpoint path in posts router
- Add proper error handling
- Update tests with correct assertions

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 트러블슈팅

### 문제 1: Command가 실행되지 않음

**증상**:
```
/test-backend
Command not found
```

**원인**: Commands 파일이 `.claude/commands/` 폴더에 없거나 형식이 잘못됨

**해결**:
```bash
# Commands 폴더 확인
ls .claude/commands/

# 파일 형식 확인 (Markdown이어야 함)
file .claude/commands/test-backend.md
```

### 문제 2: Agent가 응답하지 않음

**증상**:
```
@backend-reviewer 파일 리뷰해줘
(응답 없음)
```

**원인**: Agent 파일이 없거나 경로가 잘못됨

**해결**:
```bash
# Agents 폴더 확인
ls .claude/agents/

# Agent 파일 내용 확인
cat .claude/agents/backend-reviewer.md
```

### 문제 3: Skills가 활성화되지 않음

**증상**: Claude가 프로젝트 패턴을 따르지 않음

**원인**: Skills 파일이 없거나 YAML front matter 형식 오류

**해결**:
```bash
# Skills 폴더 확인
ls .claude/skills/

# YAML front matter 확인
head -5 .claude/skills/algo-reference-api.md
```

**올바른 형식**:
```yaml
---
name: algo-reference-api
description: FastAPI 라우터 패턴
---
```

### 문제 4: Hook이 실행되지 않음

**증상**: 파일 저장 후 자동 포맷팅이 안 됨

**원인**: `settings.local.json` 형식 오류 또는 경로 문제

**해결**:
```bash
# JSON 유효성 검사
cat .claude/settings.local.json | python -m json.tool

# Hook 로그 확인
# (Claude Code 터미널에서 확인)
```

### 문제 5: Permission 거부

**증상**:
```
Permission denied: Bash(rm -rf node_modules)
```

**원인**: `deny` 목록에 포함된 명령어

**해결**:
```json
// .claude/settings.local.json에서 수정
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)"  // 이 규칙이 차단
    ]
  }
}
```

안전한 대안:
```bash
# 직접 터미널에서 실행
rm -rf node_modules
```

### 문제 6: 마이그레이션 충돌

**증상**:
```
alembic upgrade head
Multiple heads detected
```

**해결**:
```bash
# 히스토리 확인
alembic history

# 헤드 병합
alembic merge heads -m "merge migration branches"

# 적용
alembic upgrade head
```

또는 Agent에게 문의:
```
@algo-reference-database 마이그레이션 충돌을 어떻게 해결하나요?
```

---

## FAQ

### Q1: Commands와 Skills의 차이는 무엇인가요?

**Commands**:
- 슬래시 명령어로 실행 (`/test-backend`)
- 특정 작업을 즉시 수행
- Bash 명령어 실행이 주 목적

**Skills**:
- 자동으로 활성화됨
- Claude의 응답에 프로젝트 컨텍스트 제공
- 코드 생성, 패턴 적용이 주 목적

### Q2: Agent를 언제 사용해야 하나요?

**다음 경우에 사용**:
- 코드 리뷰가 필요할 때
- 테스트 실패 원인을 분석할 때
- API 문서를 자동 생성할 때
- 이슈 해결 과정을 문서화할 때

**일반 대화로 충분한 경우**:
- 간단한 코드 수정
- 질문 답변
- 파일 읽기/쓰기

### Q3: 여러 개의 Skills가 동시에 활성화되나요?

**네, 동시 활성화됩니다!**

예: "사용자 로그인 API를 만들어줘"
- ✅ `algo-reference-architecture` (프로젝트 구조)
- ✅ `algo-reference-api` (FastAPI 패턴)
- ✅ `algo-reference-models` (SQLAlchemy 모델)

### Q4: Settings를 팀원과 공유하려면?

**방법 1: Git 커밋**
```bash
git add .claude/settings.local.json
git commit -m "Add team Claude Code settings"
git push
```

**방법 2: 문서화**
```markdown
# 팀 설정 가이드

`.claude/settings.local.json`을 다음과 같이 설정하세요:
...
```

### Q5: Backend와 Frontend를 동시에 작업할 수 있나요?

**네, 가능합니다!**

```
사용자 등록 기능을 전체 스택으로 구현해줘:
1. Backend: FastAPI 엔드포인트
2. Frontend: React 폼 컴포넌트
3. 상태 관리: Redux
```

Claude가 다음을 자동으로 생성:
- Backend API 라우터
- Pydantic 스키마
- SQLAlchemy 모델
- React 컴포넌트
- Redux slice
- 폼 검증 (Zod)

### Q6: 기존 코드를 수정하려면?

**파일 경로를 명시하세요**:
```
backend/app/api/routes/users.py의 get_user 함수에 캐싱을 추가해줘
```

Claude가:
1. 파일 읽기
2. 관련 Skills 활성화
3. 수정 사항 적용
4. 변경 내용 설명

### Q7: 에러가 발생했을 때 어떻게 하나요?

**Agent 활용**:
```
/agents run test-runner --backend
```

또는:
```
@troubleshooting-historian 이 에러의 원인과 해결 방법을 알려줘

[에러 메시지 붙여넣기]
```

### Q8: 프로젝트에 새 기능을 추가하려면?

**전체 워크플로우**:
1. 요구사항 설명
2. Claude가 설계 제안
3. 승인 후 코드 생성
4. 테스트 작성
5. 코드 리뷰 (Agent)
6. 문서 생성 (Agent)
7. 커밋

**예시**:
```
좋아요 기능을 추가하고 싶어. 다음 요구사항이 있어:
- 게시글에 좋아요/좋아요 취소
- 좋아요 수 표시
- 중복 좋아요 방지

어떻게 구현하면 좋을까?
```

---

## 다음 단계

### 1. CLAUDE.md 숙지

프로젝트 코딩 컨벤션과 워크플로우를 확인하세요:
```bash
cat CLAUDE.md
```

### 2. Commands 시도

간단한 테스트부터 시작:
```
/test-backend
/test-frontend run
```

### 3. 코드 작성 연습

Skills가 자동으로 활성화되는지 확인:
```
간단한 헬스체크 API를 만들어줘
```

### 4. Agent 활용

코드 리뷰 요청:
```
/agents run backend-reviewer backend/app/main.py
```

### 5. 문서 기여

이슈 해결 시 문서화:
```
@troubleshooting-historian [해결한 이슈 설명]
```

---

## 추가 리소스

### 공식 문서

- **Claude Code 공식 문서**: https://docs.anthropic.com/claude/docs/claude-code
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **React 문서**: https://react.dev/
- **Ant Design 문서**: https://ant.design/

### 프로젝트 문서

- **CLAUDE.md**: 개발 가이드
- **backend/README.md**: Backend 상세
- **frontend/README.md**: Frontend 상세
- **issue/**: 이슈 해결 기록
- **docs/**: 프로젝트 설계 문서

### 커뮤니티

- **팀 Slack**: #algo-reference 채널
- **GitHub Issues**: 버그 리포트 및 기능 요청
- **Wiki**: 팀 지식 베이스

---

**마지막 업데이트**: 2026-02-12
**작성자**: Claude Code Setup Automation
**버전**: 1.0.0

궁금한 점이 있으면 언제든지 Claude에게 물어보세요! 🚀
