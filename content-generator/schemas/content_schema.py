"""
Pydantic schema for algorithm content validation.

Ensures AI-generated content meets quality standards before database insertion.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List
import re


class CoreFormula(BaseModel):
    """Core formula or pattern for an algorithm."""

    name: str = Field(..., min_length=5, description="Pattern/formula name")
    formula: str = Field(..., min_length=10, description="Pseudocode or mathematical representation")
    description: str = Field(..., min_length=20, description="When and why to use this pattern")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v.strip() != v:
            raise ValueError("Name should not have leading/trailing whitespace")
        return v


class ApplicationConditions(BaseModel):
    """When to use and when not to use this algorithm."""

    when_to_use: List[str] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="Specific conditions where this algorithm is appropriate"
    )
    when_not_to_use: List[str] = Field(
        ...,
        min_length=2,
        max_length=3,
        description="Situations where this algorithm is inefficient"
    )

    @field_validator('when_to_use', 'when_not_to_use')
    @classmethod
    def validate_conditions(cls, v: List[str]) -> List[str]:
        for condition in v:
            if len(condition.strip()) < 10:
                raise ValueError(f"Condition too short: {condition}")
            if condition.lower().startswith(('use when', 'don\'t use when')):
                raise ValueError(f"Condition should not start with 'use when': {condition}")
        return v


class ProblemType(BaseModel):
    """Representative problem type with LeetCode examples."""

    type: str = Field(..., min_length=5, description="Problem pattern name")
    leetcode_examples: List[str] = Field(
        ...,
        min_length=2,
        description="LeetCode problem examples (format: 'LC 1. Two Sum')"
    )

    @field_validator('leetcode_examples')
    @classmethod
    def validate_leetcode_format(cls, v: List[str]) -> List[str]:
        leetcode_pattern = re.compile(r'^LC \d+\. .+')
        for example in v:
            if not leetcode_pattern.match(example):
                raise ValueError(
                    f"LeetCode example must match format 'LC <number>. <title>': {example}"
                )
        return v


class CodeTemplates(BaseModel):
    """Code templates in multiple languages."""

    python: str = Field(..., min_length=100, description="Python template with type hints")
    cpp: str = Field(..., min_length=100, description="C++17 template")
    java: str = Field(..., min_length=100, description="Java 11+ template")

    @field_validator('python')
    @classmethod
    def validate_python_code(cls, v: str) -> str:
        # Basic validation: should contain def and return
        if 'def ' not in v:
            raise ValueError("Python template must contain function definition")
        if 'return' not in v and 'yield' not in v:
            raise ValueError("Python template should contain return or yield statement")
        if '# TODO' in v or '# ...' in v:
            raise ValueError("Python template should not contain TODO placeholders")
        return v

    @field_validator('cpp')
    @classmethod
    def validate_cpp_code(cls, v: str) -> str:
        # Basic validation: should contain function signature
        if '{' not in v or '}' not in v:
            raise ValueError("C++ template must contain function body with braces")
        if 'TODO' in v.upper():
            raise ValueError("C++ template should not contain TODO placeholders")
        return v

    @field_validator('java')
    @classmethod
    def validate_java_code(cls, v: str) -> str:
        # Basic validation: should contain class and method
        if 'class ' not in v and 'public ' not in v:
            raise ValueError("Java template should contain class or public method")
        if '{' not in v or '}' not in v:
            raise ValueError("Java template must contain code blocks with braces")
        if 'TODO' in v.upper():
            raise ValueError("Java template should not contain TODO placeholders")
        return v


class AlgorithmContent(BaseModel):
    """Complete algorithm content following 8-point structure."""

    title: str = Field(..., min_length=5, description="Algorithm title")
    category: str = Field(..., min_length=3, description="Algorithm category")
    difficulty: str = Field(..., pattern=r'^(Easy|Medium|Hard)$', description="Difficulty level")

    concept_summary: str = Field(
        ...,
        min_length=100,
        max_length=600,
        description="1-2 paragraph explanation of the algorithm"
    )

    core_formulas: List[CoreFormula] = Field(
        ...,
        min_length=2,
        max_length=4,
        description="Key formulas/patterns"
    )

    thought_process: str = Field(
        ...,
        min_length=200,
        description="Step-by-step approach to applying the algorithm"
    )

    application_conditions: ApplicationConditions = Field(
        ...,
        description="When to use and when not to use"
    )

    time_complexity: str = Field(
        ...,
        pattern=r'O\(.+\)',
        description="Time complexity with explanation"
    )

    space_complexity: str = Field(
        ...,
        pattern=r'O\(.+\)',
        description="Space complexity with explanation"
    )

    problem_types: List[ProblemType] = Field(
        ...,
        min_length=3,
        description="Representative problem types with examples"
    )

    common_mistakes: str = Field(
        ...,
        min_length=150,
        description="Common pitfalls and how to avoid them"
    )

    code_templates: CodeTemplates = Field(
        ...,
        description="Code templates in Python, C++, Java"
    )

    @field_validator('concept_summary')
    @classmethod
    def validate_concept_summary(cls, v: str) -> str:
        if v.count('.') < 2:
            raise ValueError("Concept summary should have at least 2 sentences")
        if any(word in v.lower() for word in ['very efficient', 'commonly used', 'well-known']):
            raise ValueError("Avoid vague phrases like 'very efficient' or 'commonly used'")
        return v

    @field_validator('thought_process')
    @classmethod
    def validate_thought_process(cls, v: str) -> str:
        # Should have numbered steps or clear structure
        has_numbers = any(char.isdigit() for char in v[:100])
        has_bullets = any(marker in v for marker in ['- ', '* ', '• '])
        if not (has_numbers or has_bullets):
            raise ValueError("Thought process should use numbered steps or bullet points")
        return v

    @field_validator('common_mistakes')
    @classmethod
    def validate_common_mistakes(cls, v: str) -> str:
        if v.count('❌') < 2 or v.count('✅') < 2:
            raise ValueError("Common mistakes should use ❌ and ✅ markers for clarity")
        if 'be careful' in v.lower() or 'watch out' in v.lower():
            raise ValueError("Avoid vague warnings; be specific about mistakes")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Two Pointer Technique",
                "category": "Two Pointer",
                "difficulty": "Medium",
                "concept_summary": "The Two Pointer technique uses two pointers to traverse data structures in a coordinated manner. It's particularly effective for problems involving sorted arrays or linked lists where we need to find pairs, triplets, or validate properties. The key insight is reducing O(n²) brute force solutions to O(n) by intelligently moving pointers based on problem constraints.",
                "core_formulas": [
                    {
                        "name": "Opposite Direction Pointers",
                        "formula": "left = 0, right = n-1; while left < right: process(arr[left], arr[right]); move pointers based on comparison",
                        "description": "Start from both ends and converge toward center. Use when searching for pairs in sorted arrays, palindrome validation, or container problems. Move pointers based on target comparison."
                    },
                    {
                        "name": "Same Direction Pointers",
                        "formula": "slow = 0, fast = 0; while fast < n: if condition: slow += 1; fast += 1",
                        "description": "Both pointers move in same direction at different speeds. Use for in-place array modifications, partitioning, or slow-fast cycle detection. Fast pointer explores ahead while slow pointer maintains valid state."
                    }
                ],
                "thought_process": "1. Recognition: Look for sorted arrays, pairs/triplets with target sum, palindrome checks, or in-place modifications.\n2. Setup: Initialize two pointers (opposite ends or same start) based on problem pattern.\n3. Main Loop: While pointers haven't crossed, compare elements and decide movement.\n4. Decision Logic: If sum < target, move left pointer right; if sum > target, move right pointer left; if equal, record result.\n5. Termination: Stop when pointers meet or cross.\n6. Edge Cases: Handle empty arrays, single elements, all duplicates.",
                "application_conditions": {
                    "when_to_use": [
                        "Sorted array with pair/triplet sum target",
                        "Palindrome validation for strings or linked lists",
                        "Container with most water or trapping rain water problems",
                        "In-place array partitioning or removal of elements"
                    ],
                    "when_not_to_use": [
                        "Unsorted data requiring arbitrary access patterns",
                        "Problems needing frequency counting (use hash map instead)",
                        "When order of elements must be preserved in complex ways"
                    ]
                },
                "time_complexity": "O(n) - Single pass with two pointers traversing array once",
                "space_complexity": "O(1) - Only using two pointer variables, no extra data structures",
                "problem_types": [
                    {
                        "type": "Pair Sum in Sorted Array",
                        "leetcode_examples": [
                            "LC 167. Two Sum II - Input Array Is Sorted",
                            "LC 653. Two Sum IV - BST"
                        ]
                    },
                    {
                        "type": "Palindrome Validation",
                        "leetcode_examples": [
                            "LC 125. Valid Palindrome",
                            "LC 234. Palindrome Linked List"
                        ]
                    },
                    {
                        "type": "Container Problems",
                        "leetcode_examples": [
                            "LC 11. Container With Most Water",
                            "LC 42. Trapping Rain Water"
                        ]
                    }
                ],
                "common_mistakes": "❌ **Off-by-One Errors in Boundary Conditions**: Using `<=` instead of `<` in while loop, or incorrect initial positions. ✅ Draw examples with arrays of size 0, 1, 2 to verify.\n\n❌ **Moving Both Pointers Simultaneously**: Moving both left and right pointers in the same iteration can skip valid pairs. ✅ Only move one pointer per iteration based on comparison logic.\n\n❌ **Forgetting to Handle Duplicates**: Not skipping duplicate elements in 3Sum-like problems leads to duplicate results. ✅ Add explicit duplicate-skipping logic after finding valid results.",
                "code_templates": {
                    "python": "def two_pointer_template(arr: list[int], target: int) -> list[int]:\n    \"\"\"\n    Two pointer template for sorted array pair sum.\n    \n    Args:\n        arr: Sorted array of integers\n        target: Target sum value\n    \n    Returns:\n        Indices of two numbers that sum to target\n    \n    Time: O(n), Space: O(1)\n    \n    Example:\n        >>> two_pointer_template([2, 7, 11, 15], 9)\n        [0, 1]\n    \"\"\"\n    left, right = 0, len(arr) - 1\n    \n    while left < right:\n        current_sum = arr[left] + arr[right]\n        \n        if current_sum == target:\n            return [left, right]\n        elif current_sum < target:\n            left += 1  # Need larger sum\n        else:\n            right -= 1  # Need smaller sum\n    \n    return [-1, -1]  # No solution found",
                    "cpp": "#include <vector>\n#include <utility>\nusing namespace std;\n\npair<int, int> twoPointerTemplate(vector<int>& arr, int target) {\n    // Two pointer template for sorted array pair sum\n    // Time: O(n), Space: O(1)\n    \n    int left = 0, right = arr.size() - 1;\n    \n    while (left < right) {\n        int currentSum = arr[left] + arr[right];\n        \n        if (currentSum == target) {\n            return {left, right};\n        } else if (currentSum < target) {\n            left++;  // Need larger sum\n        } else {\n            right--;  // Need smaller sum\n        }\n    }\n    \n    return {-1, -1};  // No solution found\n}",
                    "java": "public class TwoPointerTemplate {\n    /**\n     * Two pointer template for sorted array pair sum.\n     * Time: O(n), Space: O(1)\n     * \n     * @param arr Sorted array of integers\n     * @param target Target sum value\n     * @return Array of two indices that sum to target\n     */\n    public int[] twoPointerTemplate(int[] arr, int target) {\n        int left = 0, right = arr.length - 1;\n        \n        while (left < right) {\n            int currentSum = arr[left] + arr[right];\n            \n            if (currentSum == target) {\n                return new int[]{left, right};\n            } else if (currentSum < target) {\n                left++;  // Need larger sum\n            } else {\n                right--;  // Need smaller sum\n            }\n        }\n        \n        return new int[]{-1, -1};  // No solution found\n    }\n}"
                }
            }
        }
    }


def validate_algorithm_content(content_dict: dict) -> tuple[bool, str]:
    """
    Validate algorithm content against schema.

    Args:
        content_dict: Dictionary containing algorithm content

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        AlgorithmContent(**content_dict)
        return True, "Validation successful"
    except Exception as e:
        return False, str(e)
