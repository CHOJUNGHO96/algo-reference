# 데이터베이스 마이그레이션 생성

Alembic을 사용하여 데이터베이스 마이그레이션을 생성하고 적용합니다.

## 사용법

```
/migration-create [설명]
```

## 예시

```bash
# 새 마이그레이션 생성
/migration-create "add user email field"

# 마이그레이션 적용
/migration-create apply

# 현재 리비전 확인
/migration-create current

# 마이그레이션 히스토리 확인
/migration-create history
```

## 실행 과정

### 새 마이그레이션 생성 (autogenerate)

1. backend 디렉토리로 이동
2. 현재 모델과 DB 스키마 비교
3. 차이점을 자동으로 감지하여 마이그레이션 파일 생성
4. `backend/alembic/versions/` 폴더에 파일 생성

### 마이그레이션 적용

1. 생성된 마이그레이션 파일 검토
2. `alembic upgrade head` 명령으로 적용
3. 현재 리비전 확인

## 명령어

```bash
# 새 마이그레이션 생성
cd backend && alembic revision --autogenerate -m "${MESSAGE}"

# 마이그레이션 적용
cd backend && alembic upgrade head

# 현재 리비전 확인
cd backend && alembic current

# 히스토리 확인
cd backend && alembic history

# 1단계 롤백
cd backend && alembic downgrade -1
```

## 주의사항

⚠️ **마이그레이션 적용 전 반드시 확인**:
1. 생성된 마이그레이션 파일 검토
2. 백업 데이터가 있는지 확인
3. 개발 환경에서 먼저 테스트

⚠️ **프로덕션 마이그레이션**:
- 배포 전 테스트 환경에서 검증
- 데이터베이스 백업 필수
- 롤백 계획 수립

## 출력 예시

```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'users.email'
  Generating D:\workspace_2\algo-reference\backend\alembic\versions\abc123_add_user_email_field.py ... done
```

## 관련 명령어

- `/test-backend`: 마이그레이션 후 테스트 실행
