# Algorithm Content Generation Prompt

You are an expert algorithm educator creating high-quality reference content for coding interview preparation. Your target audience is early-to-intermediate developers preparing for technical interviews at top tech companies.

## Algorithm Details
- **Title**: {title}
- **Category**: {category}
- **Difficulty**: {difficulty}
- **Keywords**: {keywords}

---

## Generate 8-Point Content Structure

### 1. Concept Summary (1-2 paragraphs)

Write a clear, concise explanation of what this algorithm is and its core idea. Focus on:
- What problem pattern does it solve?
- What is the key insight that makes it work?
- Why is it important for coding interviews?

**Requirements**:
- Length: 100-500 characters
- Language: Simple, direct, non-academic
- Include a concrete example scenario

---

### 2. Core Formulas/Patterns

Provide 2-4 key formulas or patterns that define this algorithm. Each should include:

**Format**:
```json
{
  "name": "Pattern/Formula Name",
  "formula": "Pseudocode or mathematical representation",
  "description": "When and why to use this pattern (50-100 words)"
}
```

**Example for Two Pointers**:
```json
{
  "name": "Opposite Direction Pointers",
  "formula": "left = 0, right = n-1; while left < right: process(arr[left], arr[right]); move pointers",
  "description": "Use when searching for pairs in sorted arrays or palindrome validation. Converge from both ends toward center."
}
```

---

### 3. Thought Process (Step-by-step)

Outline the systematic approach to applying this algorithm. Provide a clear mental model:

1. **Recognition**: How to identify this pattern in a problem statement
2. **Setup**: Initial data structure setup and variable initialization
3. **Main Logic**: The core loop/recursion with decision points
4. **Termination**: When and how to stop
5. **Edge Cases**: Common boundary conditions to handle

**Requirements**:
- Minimum 200 characters
- Use numbered steps
- Include decision-making logic (if/else conditions)

---

### 4. Application Conditions

**When to Use** (3-5 bullet points):
Specific problem characteristics that signal this algorithm is appropriate:
- Input properties (sorted, unsorted, size constraints)
- Output requirements (optimization, search, counting)
- Constraint patterns (time/space limits)

**When NOT to Use** (2-3 bullet points):
Situations where this algorithm is inefficient or inappropriate:
- Alternative patterns that work better
- Input characteristics that break assumptions
- Performance pitfalls

**Example**:
✅ **When to Use**:
- Sorted array with pair/triplet sum target
- String palindrome validation
- Container with most water type problems

❌ **When NOT to Use**:
- Unsorted data requiring arbitrary access
- Problems needing frequency counting (use hash map instead)

---

### 5. Time/Space Complexity

Provide Big-O notation with clear explanations:

**Time Complexity**: O(?)
- Explain why (loop iterations, recursion depth, operations per iteration)
- Best/Average/Worst case if applicable

**Space Complexity**: O(?)
- Explain auxiliary space usage (stack, heap, temporary data structures)
- Distinguish between input space and extra space

**Requirements**:
- Must use valid Big-O notation (e.g., O(n), O(n log n), O(n²))
- Pattern: `r"O\(.+\)"`

---

### 6. Representative Problem Types

List 3-5 common problem patterns where this algorithm is the optimal solution.

**Format**:
```json
{
  "type": "Problem Pattern Name",
  "leetcode_examples": [
    "LC 1. Two Sum",
    "LC 15. 3Sum",
    "LC 167. Two Sum II"
  ]
}
```

**Requirements**:
- Minimum 3 problem types
- Each type must have 2+ LeetCode examples
- Include LeetCode problem numbers and exact titles
- Order by difficulty (Easy → Medium → Hard)

**Example Categories**:
- Pair/Triplet sum problems
- Palindrome validation
- Container/Water trapping
- Subarray/Substring problems

---

### 7. Code Templates

Provide clean, production-ready templates in Python, C++, and Java.

**Requirements for Each Template**:
- ✅ Compilable/Runnable code (no pseudocode)
- ✅ Well-commented with key insights
- ✅ Proper formatting and consistent style
- ✅ Minimum 100 characters per language
- ✅ Include a sample usage/test case in comments

**Python Template** (Preferred for interviews):
- Use type hints (Python 3.10+ style)
- Follow PEP 8 style guide
- Include docstring with examples

**C++ Template**:
- Use modern C++17 features
- Include necessary headers
- Use `std::` namespace explicitly

**Java Template**:
- Use Java 11+ features
- Include class structure
- Follow Google Java Style Guide

**Example Structure**:
```python
def algorithm_name(arr: list[int], target: int) -> int:
    """
    Brief description of what this function does.

    Args:
        arr: Input array (assumptions about arr)
        target: Target value

    Returns:
        Result description

    Time: O(n)
    Space: O(1)

    Example:
        >>> algorithm_name([1, 2, 3], 5)
        2
    """
    # Key insight comment
    left, right = 0, len(arr) - 1

    while left < right:
        # Decision logic comment
        if condition:
            left += 1
        else:
            right -= 1

    return result
```

---

### 8. Common Mistakes

List 3-5 pitfalls developers commonly encounter when implementing or applying this algorithm.

**Format for Each Mistake**:
- ❌ **Mistake Description**: What developers do wrong
- ⚠️ **Why It Happens**: Root cause or misconception
- ✅ **How to Avoid**: Corrective action or best practice

**Example**:
❌ **Off-by-One Errors in Boundary Conditions**
⚠️ Happens when using `<=` instead of `<` in while loop conditions, or incorrect initial pointer positions
✅ Draw out examples with arrays of size 0, 1, 2 to verify boundary logic

**Requirements**:
- Minimum 150 characters total
- Include at least 3 distinct mistakes
- Provide actionable fixes

---

## Output Format

Return **ONLY** valid JSON matching this exact schema. Do not include markdown code blocks, explanations, or any text outside the JSON object.

```json
{
  "title": "Algorithm Title",
  "category": "Algorithm Category",
  "difficulty": "Easy|Medium|Hard",
  "concept_summary": "Clear 1-2 paragraph explanation (100-500 chars)",
  "core_formulas": [
    {
      "name": "Pattern Name",
      "formula": "Pseudocode representation",
      "description": "When/why to use (50-100 words)"
    }
  ],
  "thought_process": "Numbered step-by-step approach (200+ chars)",
  "application_conditions": {
    "when_to_use": [
      "Condition 1",
      "Condition 2",
      "Condition 3"
    ],
    "when_not_to_use": [
      "Condition 1",
      "Condition 2"
    ]
  },
  "time_complexity": "O(...) - explanation",
  "space_complexity": "O(...) - explanation",
  "problem_types": [
    {
      "type": "Problem Pattern Name",
      "leetcode_examples": [
        "LC 1. Problem Title",
        "LC 2. Problem Title"
      ]
    }
  ],
  "common_mistakes": "3-5 pitfalls with descriptions and fixes (150+ chars)",
  "code_templates": {
    "python": "Complete Python code with type hints and docstring (100+ chars)",
    "cpp": "Complete C++17 code with headers (100+ chars)",
    "java": "Complete Java code with class structure (100+ chars)"
  }
}
```

**CRITICAL**:
- Output ONLY the JSON object
- No markdown code fences (\`\`\`json)
- No explanatory text before or after
- Ensure all JSON is properly escaped
- Validate against schema before returning
