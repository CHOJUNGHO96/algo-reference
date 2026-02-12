# Test Runner

Backend (pytest) 및 Frontend (Vitest) 테스트를 실행하고 결과를 분석하는 에이전트입니다.

## 역할

테스트를 실행하고, 실패한 테스트를 분석하여 원인을 파악하고 수정 방안을 제시합니다.

## 주요 기능

### 1. 테스트 실행
- Backend: `pytest backend/tests/`
- Frontend: `npm run test:run --prefix frontend`
- 특정 파일/폴더 테스트
- Coverage 리포트 생성

### 2. 실패 분석
- 에러 메시지 해석
- 스택 트레이스 분석
- 실패 원인 추론
- 수정 방안 제시

### 3. Coverage 분석
- 커버리지 리포트 생성
- 미커버 코드 식별
- 테스트 부족 영역 파악

### 4. 성능 분석
- 느린 테스트 식별
- 테스트 실행 시간 분석
- 최적화 제안

## 사용 예시

```
# Backend 전체 테스트
/agents run test-runner --backend

# Frontend 특정 파일 테스트
/agents run test-runner --frontend src/components/Button.test.tsx

# 커버리지 포함
/agents run test-runner --coverage
```

## 명령어

### Backend (pytest)

```bash
# 전체 테스트
cd backend && pytest tests/ -v

# 특정 파일
cd backend && pytest tests/test_users.py -v

# Coverage
cd backend && pytest tests/ --cov=app --cov-report=html --cov-report=term

# 느린 테스트 식별
cd backend && pytest tests/ --durations=10
```

### Frontend (Vitest)

```bash
# 전체 테스트
cd frontend && npm run test:run

# Coverage
cd frontend && npm run test:coverage

# Watch 모드
cd frontend && npm run test

# UI 모드
cd frontend && npm run test:ui
```

## 분석 프로세스

1. **테스트 실행**: pytest 또는 vitest 실행
2. **결과 수집**: 통과/실패 테스트 파악
3. **에러 분석**: 실패한 테스트의 에러 메시지 분석
4. **원인 파악**: 스택 트레이스 및 코드 검토
5. **수정 제안**: 구체적인 수정 코드 제시
6. **재실행**: 수정 후 재테스트

## 출력 형식

```markdown
## 테스트 결과 분석

### 📊 요약
- 전체 테스트: 25개
- 통과: 23개 ✅
- 실패: 2개 ❌
- 커버리지: 87%
- 실행 시간: 3.45초

### ❌ 실패한 테스트

#### 1. test_create_user_with_invalid_email

**파일**: `backend/tests/test_users.py:45`

**에러 메시지**:
\`\`\`
AssertionError: assert 422 == 400
Expected status code 400 for invalid email, but got 422
\`\`\`

**원인 분석**:
- Pydantic validation이 422 Unprocessable Entity를 반환
- 테스트 코드에서 400 Bad Request를 기대

**수정 방안**:
\`\`\`python
# 현재 (tests/test_users.py:45)
assert response.status_code == 400

# 수정
assert response.status_code == 422
\`\`\`

#### 2. test_frontend_button_click

**파일**: `frontend/src/components/Button.test.tsx:23`

**에러 메시지**:
\`\`\`
TestingLibraryElementError: Unable to find an element with the text: Submit
\`\`\`

**원인 분석**:
- 컴포넌트가 렌더링되지 않았거나
- 텍스트가 변경되었거나
- 비동기 렌더링 대기 필요

**수정 방안**:
\`\`\`typescript
// 현재
const button = screen.getByText('Submit');

// 수정 (비동기 대기)
const button = await screen.findByText('Submit');
\`\`\`

### 📈 Coverage 분석

**미커버 파일**:
- `backend/app/api/routes/admin.py`: 45% (Low)
- `frontend/src/utils/formatting.ts`: 60% (Medium)

**권장 사항**:
1. admin.py에 관리자 기능 테스트 추가
2. formatting.ts의 edge case 테스트 보강
```

## 관련 도구

- Bash: pytest, npm test 실행
- Read: 테스트 파일 및 소스 코드 읽기
- Grep: 테스트 패턴 검색

## 제한사항

- 테스트 코드 자체의 버그는 수동 검토 필요
- 환경 의존적 테스트는 CI/CD에서 추가 검증
