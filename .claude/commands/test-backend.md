# Backend 테스트 실행

Backend pytest 테스트를 실행합니다.

## 사용법

```
/test-backend
/test-backend [테스트 파일 또는 패턴]
```

## 예시

```bash
# 전체 테스트
/test-backend

# 특정 파일
/test-backend tests/test_users.py

# 커버리지 포함
/test-backend --coverage
```

## 실행 과정

1. backend 디렉토리로 이동
2. pytest 실행 (verbose 모드)
3. 실패한 테스트가 있으면 상세 오류 출력
4. 커버리지 옵션 사용 시 HTML 리포트 생성

## 명령어

```bash
cd backend && pytest tests/ -v --tb=short ${ARGS}
```

커버리지 포함:
```bash
cd backend && pytest tests/ -v --cov=app --cov-report=html --cov-report=term ${ARGS}
```

## 출력 예시

```
============================= test session starts ==============================
platform win32 -- Python 3.11.0, pytest-7.4.0
collected 15 items

tests/test_users.py::test_create_user PASSED                             [  6%]
tests/test_users.py::test_get_user PASSED                                [ 13%]
tests/test_users.py::test_update_user PASSED                             [ 20%]

============================== 15 passed in 2.34s ===============================
```

## 관련 명령어

- `/test-frontend`: Frontend 테스트
- `/migration-create`: DB 마이그레이션 생성
