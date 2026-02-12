# Frontend 테스트 실행

Frontend Vitest 테스트를 실행합니다.

## 사용법

```
/test-frontend
/test-frontend [옵션]
```

## 예시

```bash
# 전체 테스트 (watch 모드)
/test-frontend

# 1회 실행
/test-frontend run

# 커버리지 포함
/test-frontend coverage

# UI 모드
/test-frontend ui
```

## 실행 과정

1. frontend 디렉토리로 이동
2. npm run test 명령 실행
3. 옵션에 따라 적절한 스크립트 선택

## 명령어

```bash
# Watch 모드 (기본)
cd frontend && npm run test

# 1회 실행
cd frontend && npm run test:run

# 커버리지
cd frontend && npm run test:coverage

# UI 모드
cd frontend && npm run test:ui
```

## 출력 예시

```
✓ src/components/Button.test.tsx (2)
  ✓ Button component (2)
    ✓ renders with label
    ✓ calls onClick when clicked

Test Files  1 passed (1)
     Tests  2 passed (2)
  Start at  11:23:45
  Duration  1.23s (transform 234ms, setup 0ms, collect 567ms, tests 89ms)
```

## 관련 명령어

- `/test-backend`: Backend 테스트
- `/lint-fix`: ESLint 자동 수정
