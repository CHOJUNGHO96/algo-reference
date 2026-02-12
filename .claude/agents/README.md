# 알고리즘 콘텐츠 생성 에이전트

이 디렉토리에는 알고리즘 참고 자료를 자동 생성하는 Claude Code 서브에이전트들이 있습니다.

## 에이전트 목록

### 1. algorithm-generator-part1
- **담당**: 알고리즘 1-10번
- **파일**: `algorithm-generator-part1.md`
- **메모리**: `.claude/agent-memory/algorithm-generator-part1/`

### 2. algorithm-generator-part2
- **담당**: 알고리즘 11-20번
- **파일**: `algorithm-generator-part2.md`
- **메모리**: `.claude/agent-memory/algorithm-generator-part2/`

## 사용 방법

### 병렬 실행 (권장)

두 에이전트를 동시에 실행하여 빠르게 생성:

```
Use algorithm-generator-part1 and algorithm-generator-part2 in parallel to generate all 20 algorithms
```

또는 개별 실행:

```
# 터미널 1
algorithm-generator-part1 에이전트로 1-10번 알고리즘 생성

# 터미널 2 (동시에)
algorithm-generator-part2 에이전트로 11-20번 알고리즘 생성
```

### 순차 실행

하나씩 실행:

```bash
# Part 1 먼저
Use algorithm-generator-part1 to generate algorithms 1-10

# Part 1 완료 후 Part 2
Use algorithm-generator-part2 to generate algorithms 11-20
```

### 진행 상태 확인

```
# Part 1 진행 상태
Check the memory of algorithm-generator-part1

# Part 2 진행 상태
Check the memory of algorithm-generator-part2
```

### 중단 후 재개

```
# Part 1 재개
Resume algorithm-generator-part1 and continue from where it stopped

# Part 2 재개
Resume algorithm-generator-part2 and continue from where it stopped
```

## 생성 결과

생성된 파일 위치: `content-generator/generated/`

각 알고리즘은 다음 형식으로 저장됩니다:
- `two-pointer-technique.json`
- `sliding-window.json`
- `binary-search-template.json`
- ...

## 품질 검증

모든 알고리즘 생성 후:

```bash
# Python 검증 스크립트 실행
cd content-generator
python validate_content.py
```

## 메모리 구조

각 에이전트는 독립적인 메모리를 유지합니다:

```
.claude/agent-memory/
├── algorithm-generator-part1/
│   └── MEMORY.md  (1-10번 진행 상태)
└── algorithm-generator-part2/
    └── MEMORY.md  (11-20번 진행 상태)
```

## 트러블슈팅

### 에이전트가 안 보일 때
```bash
# Claude Code 재시작
# 또는 /agents 명령으로 새로고침
/agents
```

### 생성 실패 시
1. 에이전트 메모리 확인
2. 실패 원인 파악
3. 해당 알고리즘만 재생성 요청

### 병렬 실행 충돌 시
- 각 에이전트는 다른 알고리즘을 담당하므로 충돌 없음
- 만약 같은 파일에 쓰기 시도하면 Claude Code가 자동 처리

## 예상 소요 시간

- **Part 1** (10개): 약 30-40분
- **Part 2** (10개): 약 30-40분
- **병렬 실행**: 약 30-40분 (거의 절반 시간)

## 다음 단계

모든 알고리즘 생성 완료 후:
1. `python validate_content.py` 실행
2. 생성된 JSON 파일 검토
3. 백엔드 시드 데이터로 변환
4. 데이터베이스에 삽입

---

**생성 일자**: 2026-02-12
**버전**: 1.0
