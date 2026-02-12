# Database Seeding Instructions

**Status:** Ready to seed 3 algorithms + 9 code templates

**Prerequisites:** Docker Desktop running, database migrations complete

---

## Quick Start

```bash
# Navigate to project root
cd D:\workspace_2\algo-reference

# Start services
docker-compose up -d

# Wait 30 seconds for database initialization
timeout 30

# Run seeding
docker-compose exec backend python -m scripts.seed_data
```

---

## Step-by-Step Instructions

### 1. Ensure Docker is Running

**Windows:**
- Open Docker Desktop
- Wait for "Docker Desktop is running" status
- Verify in system tray

**Verify:**
```bash
docker --version
docker-compose --version
```

### 2. Start Services

```bash
cd D:\workspace_2\algo-reference
docker-compose up -d
```

**Expected output:**
```
Creating network "algo-reference_default" with the default driver
Creating algo-reference_postgres_1 ... done
Creating algo-reference_backend_1  ... done
```

**Wait 30 seconds** for database initialization and migrations.

### 3. Run Database Seeding

```bash
docker-compose exec backend python -m scripts.seed_data
```

**Expected output:**
```
============================================================
DATABASE SEEDING - Algorithm Reference Platform
============================================================

[INFO] Found 3 algorithm files

[1/4] Seeding base reference data...
   Created difficulty: Easy
   Created difficulty: Medium
   Created difficulty: Hard
   Created language: Python
   Created language: C++
   Created language: Java
[OK] Base data ready: 3 difficulties, 3 languages

[2/4] Seeding 3 algorithms...

[1/3] Processing: two_pointer_technique.json
   Created category: Two Pointer
   [SUCCESS] ✅ Two Pointer Technique (3 templates)

[2/3] Processing: sliding_window.json
   Created category: Sliding Window
   [SUCCESS] ✅ Sliding Window (3 templates)

[3/3] Processing: binary_search_template.json
   Created category: Binary Search
   [SUCCESS] ✅ Binary Search Template (3 templates)

[3/4] Committing changes to database...
[OK] Changes committed successfully

[4/4] Running verification queries...
   Total algorithms in DB: 3
   Total code templates in DB: 9

[OK] Verification complete!

============================================================
SEEDING COMPLETE
============================================================

[RESULTS]
   ✅ Algorithms:      3
   ✅ Code Templates:  9
   ✅ Categories:      3
   ✅ Difficulties:    3
   ✅ Languages:       3
   ⏭️  Skipped:        0
   ❌ Errors:          0
```

### 4. Verify Database Content

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U algoref_user -d algoref
```

**Run verification queries:**
```sql
-- Count records
SELECT COUNT(*) as total_algorithms FROM algorithms;
-- Expected: 3

SELECT COUNT(*) as total_templates FROM code_templates;
-- Expected: 9

SELECT COUNT(*) as total_categories FROM categories;
-- Expected: 3

-- View algorithm details
SELECT id, title, slug, difficulty_id, is_published
FROM algorithms
ORDER BY id;

-- View categories with counts
SELECT c.name, COUNT(a.id) as algorithm_count
FROM categories c
LEFT JOIN algorithms a ON c.id = a.category_id
GROUP BY c.name;

-- View code templates
SELECT a.title, l.name as language, LENGTH(ct.code) as code_length
FROM code_templates ct
JOIN algorithms a ON ct.algorithm_id = a.id
JOIN programming_languages l ON ct.language_id = l.id
ORDER BY a.title, l.name;

-- Exit psql
\q
```

**Expected verification results:**
```
total_algorithms: 3
total_templates: 9
total_categories: 3

Algorithms:
1 | Two Pointer Technique | two_pointer_technique | 2 | t
2 | Sliding Window | sliding_window | 2 | t
3 | Binary Search Template | binary_search_template | 2 | t

Categories:
Two Pointer | 1
Sliding Window | 1
Binary Search | 1

Code Templates:
Two Pointer Technique | C++ | 1500+
Two Pointer Technique | Java | 1600+
Two Pointer Technique | Python | 1400+
(... 6 more rows)
```

---

## Troubleshooting

### Issue: Docker not running

**Symptom:**
```
error during connect: ... docker_engine: The system cannot find the file specified
```

**Solution:**
1. Start Docker Desktop
2. Wait for initialization
3. Retry `docker-compose up -d`

### Issue: Database connection failed

**Symptom:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
1. Check if postgres container is running: `docker-compose ps`
2. Wait 30 seconds after starting services
3. Check logs: `docker-compose logs postgres`
4. Restart services: `docker-compose restart postgres`

### Issue: Migration not run

**Symptom:**
```
sqlalchemy.exc.ProgrammingError: relation "algorithms" does not exist
```

**Solution:**
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Verify migrations
docker-compose exec postgres psql -U algoref_user -d algoref -c "\dt"
```

### Issue: Duplicate key error

**Symptom:**
```
sqlalchemy.exc.IntegrityError: duplicate key value violates unique constraint
```

**Solution:**
Seeding script automatically skips existing records. This is normal if re-running.

To clear database and re-seed:
```bash
docker-compose exec postgres psql -U algoref_user -d algoref <<EOF
TRUNCATE TABLE code_templates, algorithms, categories CASCADE;
EOF

docker-compose exec backend python -m scripts.seed_data
```

### Issue: Permission denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Run with admin/elevated privileges on Windows
# Or check file permissions:
chmod +x backend/scripts/seed_data.py
```

---

## Testing After Seeding

### Test Backend API

```bash
# List all algorithms
curl http://localhost:8000/api/v1/algorithms

# Get specific algorithm
curl http://localhost:8000/api/v1/algorithms/1

# Filter by category
curl "http://localhost:8000/api/v1/algorithms?category_id=1"

# Get categories
curl http://localhost:8000/api/v1/categories
```

**Expected API response example:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Two Pointer Technique",
      "slug": "two_pointer_technique",
      "category_id": 1,
      "difficulty_id": 2,
      "concept_summary": "The Two Pointer technique uses...",
      "is_published": true
    }
  ],
  "total": 3
}
```

### Test Frontend (if running)

```bash
# Start frontend dev server
cd frontend
npm run dev

# Open browser
http://localhost:5173
```

**Expected:**
- Algorithm listing page shows 3 cards
- Click card navigates to detail page
- Detail page shows 8-point structure
- Code templates display in 3 languages

---

## Re-running Seeding

**Safe to re-run** - Script skips existing records:
```bash
docker-compose exec backend python -m scripts.seed_data
```

**Expected on re-run:**
```
[SKIP] Already exists: Two Pointer Technique
[SKIP] Already exists: Sliding Window
[SKIP] Already exists: Binary Search Template

[RESULTS]
   ✅ Algorithms:      0
   ⏭️  Skipped:        3
```

---

## Success Criteria

After successful seeding:

✅ **Database has 3 algorithms**
✅ **Database has 9 code templates** (3 algorithms × 3 languages)
✅ **Database has 3 categories**
✅ **Database has 3 difficulty levels**
✅ **Database has 3 programming languages**
✅ **API endpoints return data**
✅ **Frontend can display algorithms**

---

## Next Steps After Seeding

1. **Notify QA Team**
   - Database ready for integration tests
   - 3 algorithms with complete data
   - API endpoints testable

2. **Notify Frontend Team**
   - Real data available via API
   - Can test listing/detail pages
   - Code templates ready for display

3. **Notify Team Lead**
   - Phase 2 content complete
   - Database seeded successfully
   - Ready for development sprint

---

**Created:** February 11, 2026

**Status:** Ready to execute (waiting for Docker)

**Time Required:** ~2 minutes (if Docker running)

**Risk:** Low - script has duplicate detection and rollback
