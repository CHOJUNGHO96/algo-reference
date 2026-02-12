# 알고리즘 콘텐츠 생성기

Claude Code 서브에이전트를 사용하여 20개 알고리즘 참고 자료를 자동 생성합니다.

## 🎯 개요

이 디렉토리는 알고리즘 학습 플랫폼을 위한 고품질 콘텐츠를 AI로 자동 생성하는 시스템입니다.

**생성 방식**: Claude Code 서브에이전트 (Python 스크립트 없음, AI 기반 자동화)

## 📂 디렉토리 구조

```
content-generator/
├── algorithm_catalog.json      # 20개 알고리즘 목록
├── prompts/
│   ├── algorithm_prompt.md     # 콘텐츠 생성 프롬프트 (한글)
│   └── validation_rules.md     # 품질 검증 규칙 (한글)
├── generated/                  # 생성된 JSON 파일 저장 위치
└── README.md                   # 이 파일
```

## 🚀 사용 방법

### 1단계: 서브에이전트 확인

Claude Code에서 다음 에이전트가 설치되어 있는지 확인:

```bash
# 에이전트 목록 보기
/agents

# 확인할 에이전트:
# - algorithm-generator-part1 (알고리즘 1-10번)
# - algorithm-generator-part2 (알고리즘 11-20번)
```

에이전트 파일 위치: `.claude/agents/`

### 2단계: 병렬 생성 실행 (권장)

```
Use algorithm-generator-part1 and algorithm-generator-part2 in parallel to generate all 20 algorithms
```

### 3단계: 진행 상태 확인

```
Check algorithm-generator-part1 memory
Check algorithm-generator-part2 memory
```

### 4단계: 생성 결과 확인

```bash
# 생성된 파일 목록
ls content-generator/generated/

# 예상 파일:
# - two-pointer-technique.json
# - sliding-window.json
# - binary-search-template.json
# - ... (총 20개)
```

## 📋 20개 알고리즘 목록

### Part 1 (1-10번)
1. Two Pointer Technique
2. Sliding Window
3. Binary Search Template
4. Depth-First Search (DFS)
5. Breadth-First Search (BFS)
6. Dynamic Programming - 1D DP
7. Dynamic Programming - 2D DP
8. Greedy Algorithm Pattern
9. Union-Find
10. Topological Sort

### Part 2 (11-20번)
11. Dijkstra's Algorithm
12. Trie
13. Heap & Priority Queue
14. Monotonic Stack
15. Fast & Slow Pointers
16. Backtracking Template
17. Prefix Sum
18. Kadane's Algorithm
19. Merge Intervals
20. Bit Manipulation Patterns

## 📐 8가지 콘텐츠 구조

각 알고리즘은 다음 구조로 생성됩니다:

1. **개념 요약** - 한 문단 설명 (100-500자)
2. **핵심 공식/패턴** - 2-4개 패턴
3. **사고 과정** - 단계별 접근법 (200자 이상)
4. **적용 조건** - 언제 사용/사용하지 말까
5. **시간/공간 복잡도** - Big-O 표기법
6. **대표 문제 유형** - 3개 이상 LeetCode 예시
7. **코드 템플릿** - Python, C++, Java
8. **주의사항** - 3-5개 함정

## ⏱️ 예상 소요 시간

- **순차 실행**: 60-80분
- **병렬 실행**: 30-40분 (권장)

## 🔍 품질 기준

생성된 콘텐츠는 다음 기준을 충족합니다:

- ✅ 모든 필수 필드 존재
- ✅ 길이 제약 준수 (개념 요약 100-500자 등)
- ✅ 유효한 Big-O 표기법
- ✅ LeetCode 문제 형식 (LC 숫자. 제목)
- ✅ 실행 가능한 코드 템플릿 (100자 이상)

## 📝 생성 예시

```json
{
  "title": "Two Pointer Technique",
  "category": "Two Pointer",
  "difficulty": "Medium",
  "concept_summary": "두 개의 포인터를 사용하여 배열이나 문자열을 효율적으로 탐색하는 기법...",
  "core_formulas": [
    {
      "name": "반대 방향 포인터",
      "formula": "left = 0, right = n-1; while left < right: ...",
      "description": "정렬된 배열에서 쌍을 찾을 때 사용..."
    }
  ],
  "thought_process": "1. 인식: 정렬된 배열, 쌍/삼중 찾기...",
  "application_conditions": {
    "when_to_use": ["정렬된 배열", "회문 검증", ...],
    "when_not_to_use": ["빈도 수 세기", ...]
  },
  "time_complexity": "O(n) - 포인터가 각각 한 번씩 이동",
  "space_complexity": "O(1) - 추가 공간 불필요",
  "problem_types": [
    {
      "type": "쌍 찾기",
      "leetcode_examples": ["LC 1. Two Sum", "LC 15. 3Sum"]
    }
  ],
  "common_mistakes": "1. Off-by-One 에러...",
  "code_templates": {
    "python": "def two_pointer(arr: list[int]) -> int:\n    ...",
    "cpp": "class Solution {\n    int twoPointer(vector<int>& arr) {...}\n};",
    "java": "class Solution {\n    public int twoPointer(int[] arr) {...}\n}"
  }
}
```

## 🔄 중단 후 재개

생성 중 중단된 경우:

```
Resume algorithm-generator-part1 and continue from where it stopped
Resume algorithm-generator-part2 and continue from where it stopped
```

각 에이전트는 진행 상태를 메모리에 저장하여 정확히 중단한 위치에서 재개합니다.

## 📊 다음 단계

모든 알고리즘 생성 완료 후:

1. **검증**: 생성된 JSON 파일 검토
2. **변환**: 백엔드 시드 데이터 형식으로 변환
3. **삽입**: 데이터베이스에 삽입
4. **테스트**: 프론트엔드에서 표시 확인

## 🛠️ 트러블슈팅

### 에이전트가 안 보일 때
```bash
# Claude Code 재시작 또는
/agents
```

### 생성 실패 시
```
Check algorithm-generator-part1 memory
# 실패 원인 확인 후 해당 알고리즘만 재생성
```

### 파일 충돌 시
- 각 에이전트는 다른 알고리즘을 담당하므로 충돌 없음

---

**생성 일자**: 2026-02-12
**방식**: Claude Code 서브에이전트
**언어**: 한글
