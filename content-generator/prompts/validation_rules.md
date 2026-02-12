# Content Quality Validation Rules

## Purpose
Ensure all AI-generated algorithm content meets quality standards for production use.

---

## Quality Criteria

### 1. Concept Summary
- ✅ Length: 100-500 characters
- ✅ Contains concrete example
- ✅ Explains "why" not just "what"
- ✅ Accessible to intermediate developers
- ❌ No academic jargon without explanation
- ❌ No vague statements ("very efficient", "commonly used")

### 2. Core Formulas
- ✅ 2-4 formulas per algorithm
- ✅ Each has name, formula, description
- ✅ Pseudocode is clear and executable
- ✅ Description explains when/why (50-100 words)
- ❌ No mathematical notation without context
- ❌ No formulas without practical application

### 3. Thought Process
- ✅ Minimum 200 characters
- ✅ Uses numbered steps (5-7 steps ideal)
- ✅ Includes recognition patterns
- ✅ Covers edge cases
- ✅ Decision logic is explicit
- ❌ No high-level hand-waving
- ❌ No "it's obvious" assumptions

### 4. Application Conditions
- ✅ 3-5 "when to use" conditions
- ✅ 2-3 "when NOT to use" conditions
- ✅ Specific input/output characteristics
- ✅ Mentions alternative patterns
- ❌ No generic advice ("use when fast solution needed")
- ❌ No contradictory conditions

### 5. Complexity Analysis
- ✅ Valid Big-O notation (matches regex: `O\(.+\)`)
- ✅ Explains reasoning (loop counts, recursion depth)
- ✅ Distinguishes time vs. space
- ✅ Mentions best/average/worst if applicable
- ❌ No unexplained notation
- ❌ No incorrect complexity claims

### 6. Problem Types
- ✅ 3-5 representative problem types
- ✅ Each type has 2+ LeetCode examples
- ✅ Includes problem numbers and exact titles
- ✅ Ordered by difficulty
- ✅ Covers diverse applications
- ❌ No made-up problem titles
- ❌ No duplicate examples across types

### 7. Code Templates
- ✅ All 3 languages: Python, C++, Java
- ✅ Each template ≥100 characters
- ✅ Compilable/runnable code (no pseudocode)
- ✅ Well-commented with key insights
- ✅ Includes sample usage in comments
- ✅ Proper formatting and style
- ❌ No syntax errors
- ❌ No placeholder comments ("// TODO")
- ❌ No inconsistent naming across languages

#### Python Requirements
- Type hints (Python 3.10+)
- Docstring with example
- PEP 8 compliant
- Handles edge cases

#### C++ Requirements
- Modern C++17 features
- Necessary headers included
- `std::` namespace explicit
- STL usage where appropriate

#### Java Requirements
- Java 11+ features
- Class structure included
- Google Java Style Guide
- Proper exception handling

### 8. Common Mistakes
- ✅ Minimum 150 characters total
- ✅ 3-5 distinct mistakes
- ✅ Each mistake has:
  - Description (what went wrong)
  - Root cause (why it happens)
  - Fix (how to avoid)
- ✅ Practical, interview-relevant pitfalls
- ❌ No generic warnings ("be careful")
- ❌ No mistakes that contradict templates

---

## JSON Schema Validation

### Required Fields
All fields must be present and non-empty:
- title
- category
- difficulty
- concept_summary
- core_formulas (array, 2-4 items)
- thought_process
- application_conditions (object with when_to_use, when_not_to_use)
- time_complexity
- space_complexity
- problem_types (array, 3+ items)
- common_mistakes
- code_templates (object with python, cpp, java)

### Field Constraints
- `concept_summary`: 100-500 chars
- `core_formulas`: 2-4 items, each with name/formula/description
- `thought_process`: 200+ chars
- `application_conditions.when_to_use`: 3-5 items
- `application_conditions.when_not_to_use`: 2-3 items
- `time_complexity`: matches `O\(.+\)` pattern
- `space_complexity`: matches `O\(.+\)` pattern
- `problem_types`: 3+ items, each with type and 2+ leetcode_examples
- `common_mistakes`: 150+ chars
- `code_templates.python`: 100+ chars
- `code_templates.cpp`: 100+ chars
- `code_templates.java`: 100+ chars

---

## Automated Validation Checks

### Phase 1: Schema Validation
Use Pydantic schema to validate structure and types.

### Phase 2: Content Quality Checks
- Word count validation
- Keyword presence (e.g., "O(" in complexity)
- LeetCode problem format validation (regex: `LC \d+\. .+`)
- Code syntax validation (AST parsing for Python)

### Phase 3: Manual Review Triggers
Flag for human review if:
- Complexity is O(1) or O(2^n) (uncommon, verify correctness)
- Code templates < 150 chars (likely incomplete)
- Common mistakes < 200 chars (likely generic)
- No edge case handling mentioned
- Difficulty mismatch (e.g., O(2^n) but "Easy" difficulty)

---

## Rejection Criteria

**Auto-Reject if**:
- Missing required fields
- Schema validation fails
- Code templates have syntax errors
- LeetCode examples don't match format
- Complexity notation invalid
- Content length below minimums

**Flag for Revision if**:
- Generic advice without specifics
- Contradictory statements
- Unclear explanations
- Missing edge case handling
- Code templates lack comments
- Common mistakes are vague

---

## Quality Score Rubric (0-100)

### Scoring Components
- **Clarity** (20 pts): Concept summary, thought process readability
- **Completeness** (20 pts): All 8 sections fully developed
- **Code Quality** (20 pts): Templates are production-ready
- **Practical Value** (20 pts): Real interview applicability
- **Accuracy** (20 pts): Correct complexity, valid examples

### Thresholds
- **90-100**: Excellent, publish immediately
- **75-89**: Good, minor revisions suggested
- **60-74**: Acceptable, significant improvements needed
- **<60**: Reject, regenerate with refined prompt

---

## Common AI Generation Issues

### Issue: Generic Content
**Symptom**: Vague statements like "this algorithm is useful"
**Fix**: Request specific examples and concrete scenarios

### Issue: Incorrect Complexity
**Symptom**: Claims O(n log n) but code shows O(n²)
**Fix**: Manual code review, ask AI to explain line-by-line

### Issue: Missing Edge Cases
**Symptom**: Templates don't handle empty inputs
**Fix**: Add explicit edge case requirements to prompt

### Issue: Inconsistent Code Style
**Symptom**: Python uses camelCase, Java uses snake_case
**Fix**: Enforce language-specific style guides in prompt

### Issue: Outdated LeetCode Problems
**Symptom**: Problem numbers don't exist or titles mismatch
**Fix**: Cross-reference with LeetCode API or recent problem lists

---

## Continuous Improvement

### Feedback Loop
1. Track which algorithms require manual revision
2. Identify common AI mistakes per category
3. Refine prompts based on error patterns
4. Update validation rules as patterns emerge

### Version Control
- Track prompt versions with git
- Document which algorithms were generated with which prompt version
- Regenerate outdated content with improved prompts
