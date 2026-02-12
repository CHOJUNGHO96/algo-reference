# Claude Code 빠른 시작 가이드

5분만에 Claude Code 사용법을 익혀보세요! 🚀

---

## 🎯 핵심 기능 3가지

### 1. Commands - 슬래시 명령어

자주 사용하는 작업을 슬래시 명령어로 실행하세요.

```
/test-backend              # Backend 테스트 실행
/test-frontend run         # Frontend 테스트 실행
/migration-create "설명"   # DB 마이그레이션 생성
/run-fullstack             # Docker로 전체 스택 실행
/lint-fix backend          # Backend 코드 포맷팅
```

### 2. Agents - AI 전문가

복잡한 작업은 전문 AI 에이전트에게 맡기세요.

```
/agents run backend-reviewer backend/app/api/routes/users.py
```

또는 대화형:

```
@backend-reviewer 이 파일을 리뷰해줘: backend/app/api/routes/users.py
```

**사용 가능한 Agents**:
- `backend-reviewer`: Python FastAPI 코드 리뷰
- `frontend-reviewer`: React TypeScript 코드 리뷰
- `test-runner`: 테스트 실행 및 실패 분석
- `api-doc-generator`: API 문서 자동 생성
- `troubleshooting-historian`: 이슈 해결 과정 문서화

### 3. Skills - 자동 컨텍스트

코드 작성 시 프로젝트 패턴이 **자동으로** 적용됩니다!

#### 예시: API 엔드포인트 작성

**질문**:
```
게시글 목록 조회 API를 만들어줘
```

**Claude 응답** (자동으로 프로젝트 패턴 적용):
```python
# algo-reference-api 스킬이 자동 활성화됨!
@router.get("/", response_model=List[PostResponse])
async def list_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[PostResponse]:
    """게시글 목록 조회"""
    result = await db.execute(
        select(Post).offset(skip).limit(limit).order_by(Post.created_at.desc())
    )
    return result.scalars().all()
```

---

## 📝 실전 예제

### 예제 1: 새 API 만들기 (5분)

```
1. "좋아요 기능 API를 만들어줘"
   → Claude가 모델, 스키마, 라우터 생성

2. /migration-create "add likes table"
   → 마이그레이션 생성 및 적용

3. /test-backend tests/test_likes.py
   → 테스트 실행

4. /agents run backend-reviewer backend/app/api/routes/likes.py
   → 코드 리뷰
```

### 예제 2: React 컴포넌트 만들기 (3분)

```
1. "게시글 카드 컴포넌트를 Ant Design으로 만들어줘"
   → Claude가 컴포넌트 생성 (프로젝트 패턴 자동 적용)

2. /test-frontend src/components/PostCard.test.tsx
   → 테스트 실행

3. /agents run frontend-reviewer frontend/src/components/PostCard.tsx
   → 코드 리뷰
```

### 예제 3: 버그 수정 (2분)

```
1. "게시글 삭제 시 404 에러가 나. 원인을 찾아줘"
   → Claude가 원인 분석

2. "수정해줘"
   → Claude가 코드 수정

3. /test-backend tests/test_posts.py::test_delete_post
   → 수정 확인

4. @troubleshooting-historian 이 이슈를 문서화해줘
   → 자동으로 issue/ 폴더에 문서 생성
```

---

## ⚡ 치트시트

### 자주 사용하는 Commands

| 작업 | 명령어 |
|------|--------|
| Backend 테스트 | `/test-backend` |
| Frontend 테스트 | `/test-frontend run` |
| DB 마이그레이션 | `/migration-create "설명"` |
| 전체 실행 | `/run-fullstack` |
| 코드 포맷팅 | `/lint-fix all` |

### 자주 사용하는 Agent 호출

| 작업 | 명령어 |
|------|--------|
| Backend 리뷰 | `@backend-reviewer [파일경로]` |
| Frontend 리뷰 | `@frontend-reviewer [파일경로]` |
| 테스트 분석 | `@test-runner --backend` |
| API 문서 생성 | `@api-doc-generator` |
| 이슈 문서화 | `@troubleshooting-historian [설명]` |

### 프로젝트 패턴 (자동 적용)

| 작업 | 자동 활성화되는 Skill |
|------|---------------------|
| API 엔드포인트 | `algo-reference-api` |
| DB 모델 | `algo-reference-models` |
| React 컴포넌트 | `algo-reference-components` |
| Redux 상태 관리 | `algo-reference-state` |
| 폼 검증 | `algo-reference-forms` |

---

## 🎓 다음 학습

### 초급 → 중급

1. **CLAUDE.md 읽기**: 프로젝트 코딩 컨벤션 숙지
2. **Settings 커스터마이징**: `.claude/settings.local.json` 수정
3. **Hooks 활용**: 자동 포맷팅, 테스트 실행

### 중급 → 고급

1. **상세 가이드**: `docs/CLAUDE_CODE_USAGE_GUIDE.md` 참고
2. **커스텀 Commands 추가**: `.claude/commands/` 폴더에 새 파일 생성
3. **팀 설정 공유**: Settings를 Git에 커밋하여 팀원과 공유

---

## ❓ 도움이 필요하신가요?

### 궁금한 점이 있으면 Claude에게 물어보세요!

```
Commands가 뭐야?
Agents를 어떻게 사용하나요?
Skills는 언제 활성화되나요?
```

### 상세 문서

- **전체 가이드**: `docs/CLAUDE_CODE_USAGE_GUIDE.md`
- **개발 가이드**: `CLAUDE.md`
- **이슈 기록**: `issue/` 폴더

---

**작성일**: 2026-02-12
**소요 시간**: 5분

지금 바로 시작하세요! 🎉
