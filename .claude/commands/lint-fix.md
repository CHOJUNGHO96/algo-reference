# 린트 자동 수정

Backend (Black) 및 Frontend (ESLint)의 린트 오류를 자동으로 수정합니다.

## 사용법

```
/lint-fix [대상]
```

## 예시

```bash
# Backend 린트 수정
/lint-fix backend

# Frontend 린트 수정
/lint-fix frontend

# 전체 린트 수정
/lint-fix all
```

## 실행 과정

### Backend (Black + isort)

1. `black` 포맷터로 Python 코드 자동 포맷팅
2. `isort`로 import 문 정렬 (선택)
3. `flake8`로 추가 검사 (선택)

### Frontend (ESLint + Prettier)

1. ESLint 자동 수정 실행
2. Prettier 포맷팅 적용
3. 수정 불가능한 오류 리포트

## 명령어

### Backend

```bash
# Black 포맷팅
cd backend && black app/ tests/

# isort (import 정렬)
cd backend && isort app/ tests/

# flake8 검사 (수정 없음)
cd backend && flake8 app/ tests/
```

### Frontend

```bash
# ESLint 자동 수정
cd frontend && npm run lint -- --fix

# Prettier 포맷팅
cd frontend && npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css}"

# 특정 파일
cd frontend && npx prettier --write src/components/Button.tsx
```

## 설정 파일

- **Backend**:
  - `pyproject.toml`: Black, isort 설정
  - `.flake8` 또는 `setup.cfg`: flake8 설정

- **Frontend**:
  - `eslint.config.js`: ESLint 규칙
  - `.prettierrc`: Prettier 설정

## 출력 예시

### Backend (Black)

```
reformatted app/api/routes/users.py
reformatted app/core/config.py

All done! ✨ 🍰 ✨
2 files reformatted, 15 files left unchanged.
```

### Frontend (ESLint)

```
✖ 3 problems (2 errors, 1 warning)
  2 errors and 1 warning potentially fixable with the `--fix` option.

✔ Fixed 3 problems
```

## 주의사항

⚠️ **포맷팅 전 확인**:
1. 변경사항이 많을 수 있으므로 git commit 후 실행 권장
2. 자동 수정 후 코드 동작 확인 필수
3. 팀 코딩 컨벤션과 충돌하지 않는지 확인

## 관련 명령어

- `/test-backend`: 포맷팅 후 테스트 실행
- `/test-frontend`: 린트 수정 후 테스트 실행
