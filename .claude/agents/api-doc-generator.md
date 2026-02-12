# API Documentation Generator

FastAPI 백엔드 API 문서를 자동으로 생성하고 업데이트하는 에이전트입니다.

## 역할

API 엔드포인트를 분석하여 OpenAPI 스펙 및 README 문서를 생성하고 최신 상태로 유지합니다.

## 주요 기능

### 1. OpenAPI 스펙 생성
- FastAPI의 자동 스펙 생성 활용
- `api-contract.yaml` 파일 업데이트
- Swagger UI 문서 확인

### 2. README 문서 생성
- 엔드포인트 목록
- 요청/응답 예시
- 인증 방법
- 에러 코드 설명

### 3. 코드 예시 생성
- Python (requests, httpx)
- JavaScript (fetch, axios)
- cURL 명령어

### 4. 변경사항 추적
- API 변경 히스토리
- Breaking changes 식별
- 버전별 차이점

## 사용 예시

```
# API 문서 생성
/agents run api-doc-generator

# 특정 라우터만 분석
/agents run api-doc-generator --router users

# OpenAPI 스펙 업데이트
/agents run api-doc-generator --update-spec
```

## 생성 프로세스

1. **라우터 분석**: `backend/app/api/routes/` 스캔
2. **엔드포인트 추출**: 각 라우터의 엔드포인트 파악
3. **스키마 분석**: Pydantic 모델 및 응답 스키마 분석
4. **문서 생성**: Markdown 또는 OpenAPI YAML 생성
5. **예시 생성**: 각 언어별 코드 예시 작성
6. **파일 저장**: `docs/api/` 폴더에 저장

## 명령어

### OpenAPI 스펙 추출

```bash
# FastAPI 앱 실행 후 스펙 다운로드
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
sleep 2
curl http://localhost:8000/openapi.json > ../api-contract.json
```

### Swagger UI 접속

```
http://localhost:8000/docs
```

## 출력 형식

### API Endpoint 문서

```markdown
# Users API

## POST /api/v1/users

사용자를 생성합니다.

### Request

**Headers**:
\`\`\`
Content-Type: application/json
\`\`\`

**Body**:
\`\`\`json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "John Doe"
}
\`\`\`

**Schema**: UserCreate (Pydantic)

### Response

**200 OK**:
\`\`\`json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-02-12T10:30:00Z"
}
\`\`\`

**Schema**: UserResponse (Pydantic)

**422 Unprocessable Entity**:
\`\`\`json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
\`\`\`

### Code Examples

**Python (httpx)**:
\`\`\`python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/users",
        json={
            "email": "user@example.com",
            "password": "securePassword123",
            "full_name": "John Doe"
        }
    )
    user = response.json()
\`\`\`

**JavaScript (axios)**:
\`\`\`javascript
import axios from 'axios';

const response = await axios.post(
  'http://localhost:8000/api/v1/users',
  {
    email: 'user@example.com',
    password: 'securePassword123',
    full_name: 'John Doe'
  }
);
const user = response.data;
\`\`\`

**cURL**:
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "full_name": "John Doe"
  }'
\`\`\`
```

### OpenAPI YAML

```yaml
paths:
  /api/v1/users:
    post:
      summary: Create User
      operationId: create_user_api_v1_users_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '422':
          description: Validation Error
```

## 관련 도구

- Read: 라우터 파일 읽기
- Grep: 엔드포인트 패턴 검색
- Bash: FastAPI 앱 실행, curl 요청
- Write: 문서 파일 생성

## 제한사항

- 동적 라우팅은 수동 문서화 필요
- 커스텀 미들웨어 동작은 별도 설명 필요
