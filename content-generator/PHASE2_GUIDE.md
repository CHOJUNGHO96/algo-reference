# Phase 2 Implementation Guide - AI Content Generation

Complete guide for generating 20 algorithm contents using Claude AI and seeding the database.

## Prerequisites

1. **Anthropic API Key**
   ```bash
   # Create .env file in project root
   cd /path/to/algo-reference
   cp .env.example .env

   # Add your API key
   echo "ANTHROPIC_API_KEY=your_key_here" >> .env
   ```

2. **Install Dependencies**
   ```bash
   cd content-generator
   pip install -r requirements.txt
   ```

3. **Database Running**
   ```bash
   # Ensure PostgreSQL is running via Docker
   cd ..
   docker-compose up -d postgres
   ```

## Step 1: Generate AI Content (20 Algorithms)

### Option A: Generate All 20 Algorithms

```bash
cd content-generator
python generate_algorithms.py --generate
```

**Expected Output:**
- 20 JSON files in `generated/` directory
- Cost report: ~$1-3 total (using Claude 3.5 Sonnet)
- Time: ~5-10 minutes (with rate limiting)

### Option B: Generate Single Algorithm (Testing)

```bash
python generate_algorithms.py --algorithm "Two Pointer Technique"
```

### Option C: Validation Only (No API Calls)

```bash
python generate_algorithms.py --validate
```

## Step 2: Validate Generated Content

```bash
python validate_content.py
```

**Quality Checks:**
- ✅ 8-point structure completeness (target: >90%)
- ✅ Python syntax validation
- ✅ C++/Java basic structure check
- ✅ LeetCode reference format
- ✅ No placeholder text (TODO, Lorem ipsum, etc.)

**Output Files:**
- `generated/validation_report.json` - Detailed validation results
- Console output with issue summary

## Step 3: Seed Database

### Option A: Using Docker

```bash
cd ../backend
docker-compose exec backend python -m scripts.seed_data
```

### Option B: Direct Execution

```bash
cd ../backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python -m scripts.seed_data
```

**Expected Output:**
```
[RESULTS]
   ✅ Algorithms:      20
   ✅ Code Templates:  60  (20 × 3 languages)
   ✅ Categories:      ~15 (auto-created)
   ✅ Difficulties:    3
   ✅ Languages:       3
```

## Step 4: Verify Database

### SQL Verification

```bash
# Connect to database
docker-compose exec postgres psql -U algoref_user -d algoref

# Run verification queries
SELECT COUNT(*) FROM algorithms;  -- Should be 20
SELECT COUNT(*) FROM code_templates;  -- Should be 60
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM difficulty_levels;  -- Should be 3

# Sample algorithm check
SELECT title, category_id, difficulty_id, is_published
FROM algorithms
LIMIT 5;

# Exit psql
\q
```

### API Verification

```bash
# Start backend if not running
cd backend
docker-compose up -d backend

# Test API endpoints
curl http://localhost:8000/api/v1/algorithms | jq '.total'
curl http://localhost:8000/api/v1/categories | jq '.items[].name'
```

## Cost Analysis

### Expected Costs (Claude 3.5 Sonnet)

**Pricing:**
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens

**Estimated Per Algorithm:**
- Prompt: ~3,000 tokens (input)
- Response: ~3,500 tokens (output)
- Cost: ~$0.06 per algorithm

**Total for 20 Algorithms:**
- Total tokens: ~130,000 tokens
- Total cost: **$1.00 - $1.50**

**Actual costs saved in:** `generated/cost_report.json`

## Troubleshooting

### Issue: API Key Not Found

```bash
# Check .env file exists
ls -la ../.env

# Verify key is set
grep ANTHROPIC_API_KEY ../.env
```

### Issue: Rate Limiting

**Symptom:** "rate_limit" errors during generation

**Solution:** Script has built-in exponential backoff, just wait

### Issue: Validation Failures

**Symptom:** Generated content doesn't pass Pydantic validation

**Solution:**
1. Check `generated/*.json` for the specific file
2. Read validation error messages
3. Manually fix JSON if needed
4. Re-run validation: `python validate_content.py`

### Issue: Database Connection Failed

```bash
# Check Docker containers
docker-compose ps

# Restart postgres
docker-compose restart postgres

# Check connection string in .env
grep DATABASE_URL ../.env
```

### Issue: Duplicate Key Error During Seeding

**Symptom:** "already exists" or "duplicate key" errors

**Solution:** Seeding script skips existing algorithms automatically

To force fresh seeding:
```sql
-- Connect to database
docker-compose exec postgres psql -U algoref_user -d algoref

-- Clear all data
TRUNCATE TABLE algorithms, code_templates, categories CASCADE;

-- Exit and re-run seeding
\q
```

## File Structure

```
content-generator/
├── algorithm_catalog.json         # 20 algorithms metadata
├── prompts/
│   └── algorithm_prompt.md        # AI generation template
├── schemas/
│   └── content_schema.py          # Pydantic validation
├── generated/                     # AI-generated content
│   ├── two_pointer_technique.json
│   ├── sliding_window.json
│   ├── ... (18 more)
│   ├── cost_report.json          # API usage report
│   └── validation_report.json    # Quality report
├── generate_algorithms.py         # Main generation script
├── validate_content.py            # Quality validator
└── PHASE2_GUIDE.md               # This file

backend/
└── scripts/
    └── seed_data.py               # Database seeding script
```

## Quality Standards

### Completeness Thresholds

- **Excellent:** 95-100% (all fields filled, no issues)
- **Good:** 90-95% (minor fields missing)
- **Acceptable:** 85-90% (some optional fields empty)
- **Poor:** <85% (requires manual review)

### Content Length Guidelines

- **Concept Summary:** 100-500 characters
- **Thought Process:** 200+ characters
- **Common Mistakes:** 150+ characters
- **Code Templates:** 100+ characters per language

### Code Quality

- **Python:** Must pass `ast.parse()` (syntax valid)
- **C++:** Must have includes, braces, semicolons
- **Java:** Must have class structure, braces
- **No Placeholders:** No TODO, FIXME, or Lorem ipsum

## Next Steps

After successful seeding:

1. **Test Backend API** (Task #12)
   ```bash
   curl http://localhost:8000/api/v1/algorithms
   ```

2. **Test Frontend** (Task #13)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Run E2E Tests** (Task #16)
   ```bash
   cd backend
   pytest tests/
   ```

## Success Criteria Checklist

- [ ] 20 algorithm JSON files generated
- [ ] Cost report shows $1-3 total
- [ ] Validation report shows >90% completeness
- [ ] No placeholder text in any file
- [ ] Database seeding completes without errors
- [ ] SQL queries return expected counts
- [ ] API endpoints return algorithm data
- [ ] All code templates are syntactically valid

## Support

If you encounter issues:

1. Check `generated/cost_report.json` for generation stats
2. Check `generated/validation_report.json` for quality issues
3. Review console output for specific error messages
4. Verify database connection and migrations
5. Test API endpoints manually with curl

---

**Estimated Total Time:** 15-30 minutes (including API calls and validation)

**Estimated Total Cost:** $1.00 - $1.50 (Claude 3.5 Sonnet)
