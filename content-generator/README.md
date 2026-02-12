# Algorithm Content Generator

AI-powered content generation system for algorithm reference platform.

## Overview

This module generates high-quality algorithm content following an 8-point structure:
1. Concept Summary
2. Core Formulas/Patterns
3. Thought Process
4. Application Conditions
5. Time/Space Complexity
6. Representative Problem Types
7. Code Templates (Python, C++, Java)
8. Common Mistakes

## Directory Structure

```
content-generator/
├── algorithm_catalog.json      # 20 curated algorithms with metadata
├── prompts/
│   ├── algorithm_prompt.md     # Master AI prompt template
│   ├── code_template_prompt.md # Code generation guidelines
│   └── validation_rules.md     # Content quality standards
├── schemas/
│   └── content_schema.py       # Pydantic validation schema
├── generated/                  # AI-generated JSON outputs
├── generate_algorithms.py      # Main generation script
├── requirements.txt
└── README.md                   # This file
```

## Phase 1: Preparation (Complete)

✅ **Algorithm Catalog** (`algorithm_catalog.json`)
- 20 core algorithms across 10+ categories
- Prioritized by interview frequency
- Rich metadata (difficulty, keywords, category)

✅ **AI Prompt Template** (`prompts/algorithm_prompt.md`)
- Comprehensive 8-point structure
- Detailed requirements for each section
- JSON output format specification
- Quality guidelines embedded

✅ **Validation Schema** (`schemas/content_schema.py`)
- Pydantic models for all content types
- Field-level validators (length, format, content)
- Custom validators for code quality
- Example data included

✅ **Generation Script** (`generate_algorithms.py`)
- Catalog loading and validation
- Prompt preparation
- Placeholder for AI integration
- Content validation and saving

## Phase 2: AI Generation (Upcoming)

**Implementation Steps**:
1. Set up AI API credentials (Claude 3.5 Sonnet recommended)
2. Implement `generate_algorithm_content()` function
3. Add error handling and retry logic
4. Run generation for all 20 algorithms
5. Manual review and refinement

## Usage

### Validation Mode (Phase 1)
```bash
# Install dependencies
pip install -r requirements.txt

# Run validation checks
python generate_algorithms.py --validate

# Expected output:
# ✅ Loaded 20 algorithms from catalog
# ✅ Catalog structure validation passed
# ✅ Loaded prompt template
# ✅ Prompt preparation test successful
# ✅ Output directory ready
# 🚀 Ready for Phase 2: AI content generation
```

### Generation Mode (Phase 2)
```bash
# Generate all algorithms
python generate_algorithms.py --generate

# Generate specific algorithm
python generate_algorithms.py --generate --algorithm "Two Pointer Technique"
```

## Algorithm Catalog

### Categories (20 algorithms)
- **Two Pointer** (1): Two Pointer Technique
- **Sliding Window** (1): Sliding Window
- **Binary Search** (1): Binary Search Template
- **Tree/Graph** (2): DFS, BFS
- **Dynamic Programming** (2): 1D DP, 2D DP
- **Greedy** (1): Greedy Algorithm Pattern
- **Graph** (2): Union-Find, Topological Sort, Dijkstra's
- **Tree** (1): Trie
- **Heap** (1): Heap & Priority Queue
- **Stack** (1): Monotonic Stack
- **Linked List** (1): Fast & Slow Pointers
- **Backtracking** (1): Backtracking Template
- **Array** (2): Prefix Sum, Kadane's Algorithm
- **Interval** (1): Merge Intervals
- **Bit Manipulation** (1): Bit Manipulation Patterns

### Priority Ranking
1. Two Pointer Technique
2. Sliding Window
3. Binary Search Template
4. DFS
5. BFS
6-20. Additional core patterns

## Quality Standards

### Validation Criteria
- ✅ All 8 sections complete and non-empty
- ✅ Concept summary: 100-500 chars
- ✅ Core formulas: 2-4 items with descriptions
- ✅ Thought process: 200+ chars with numbered steps
- ✅ Application conditions: 3-5 "when to use", 2-3 "when not to use"
- ✅ Complexity: Valid Big-O notation with explanations
- ✅ Problem types: 3+ types with 2+ LeetCode examples each
- ✅ Code templates: 100+ chars per language, no syntax errors
- ✅ Common mistakes: 150+ chars with specific pitfalls

### AI Model Recommendations
- **Primary**: Claude 3.5 Sonnet (best code quality, detailed explanations)
- **Alternative**: GPT-4 Turbo (good consistency, JSON mode support)
- **Cost**: ~$0.05-0.15 per algorithm (estimated)

## Phase 2 Implementation Notes

### AI API Setup
```python
# Option 1: Anthropic Claude (Recommended)
from anthropic import Anthropic

client = Anthropic(api_key="your_api_key")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}]
)
content = json.loads(response.content[0].text)

# Option 2: OpenAI GPT
from openai import OpenAI

client = OpenAI(api_key="your_api_key")
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
)
content = json.loads(response.choices[0].message.content)
```

### Error Handling
- Retry logic for API failures (3 attempts)
- Validation failures trigger prompt refinement
- Manual review queue for edge cases
- Cost tracking and budget limits

### Quality Control
1. Automated Pydantic validation
2. Code syntax checking (AST parsing)
3. LeetCode problem number verification
4. Manual review of first 3 generated algorithms
5. Iterative prompt refinement based on feedback

## Success Criteria

**Phase 1** ✅:
- [x] 20 algorithms cataloged with metadata
- [x] Comprehensive AI prompt template
- [x] Robust Pydantic validation schema
- [x] Generation script structure ready
- [x] All validation checks pass

**Phase 2** (Upcoming):
- [ ] AI API integration complete
- [ ] 20 algorithms generated and validated
- [ ] Manual review passed (≥90% quality score)
- [ ] JSON files ready for database seeding
- [ ] Cost within budget (<$5 total)

## Next Steps

1. **Set up API credentials**: Create `.env` file with `ANTHROPIC_API_KEY`
2. **Implement AI generation**: Complete `generate_algorithm_content()` function
3. **Test with single algorithm**: Validate output quality
4. **Refine prompts**: Adjust based on initial results
5. **Batch generate**: Process all 20 algorithms
6. **Manual review**: Check for accuracy and completeness
7. **Export to database**: Integration with backend seeding script

## License

Part of the Algorithm Reference Platform project.
