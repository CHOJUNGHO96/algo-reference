# Backend Quick Start Guide

## Prerequisites
- PostgreSQL 12+ installed and running
- Python 3.11+ installed
- uv package manager installed

## Quick Setup (5 minutes)

### 1. Database Setup
```bash
# Create PostgreSQL database
createdb algoref

# Or using psql
psql -U postgres
CREATE DATABASE algoref;
\q
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd D:/workspace_2/algo-reference/backend

# Activate virtual environment (already created)
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Run database migrations
alembic upgrade head

# This will create all tables and seed initial data:
# - 3 difficulty levels
# - 7 programming languages
# - 10 algorithm categories
# - 1 admin user (admin@algoref.com / admin123)
```

### 3. Start Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Base URL:** http://localhost:8000/api/v1

## Default Admin Credentials
- **Email:** admin@algoref.com
- **Password:** admin123
- ⚠️ **IMPORTANT:** Change password in production

## Testing the API

### 1. Login to get JWT token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@algoref.com", "password": "admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### 2. List Categories (No Auth Required)
```bash
curl "http://localhost:8000/api/v1/categories"
```

### 3. Create Algorithm (Admin Auth Required)
```bash
curl -X POST "http://localhost:8000/api/v1/admin/algorithms" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Two Pointer Technique",
    "category_id": 1,
    "difficulty_id": 2,
    "concept_summary": "Two pointers moving through array simultaneously",
    "time_complexity": "O(n)",
    "space_complexity": "O(1)"
  }'
```

### 4. List Algorithms
```bash
curl "http://localhost:8000/api/v1/algorithms"
```

### 5. Get Algorithm by Slug
```bash
curl "http://localhost:8000/api/v1/algorithms/two-pointer-technique"
```

## Available Endpoints

### Public Endpoints (No Auth)
- `GET /api/v1/algorithms` - List algorithms with pagination/filtering
- `GET /api/v1/algorithms/{slug}` - Get algorithm details
- `GET /api/v1/categories` - List categories
- `GET /api/v1/categories/{slug}` - Get category by slug
- `GET /api/v1/languages` - List programming languages

### Auth Endpoints
- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user (requires auth)

### Admin Endpoints (JWT Required)
- `POST /api/v1/admin/algorithms` - Create algorithm
- `PUT /api/v1/admin/algorithms/{id}` - Update algorithm
- `DELETE /api/v1/admin/algorithms/{id}` - Delete algorithm
- `POST /api/v1/admin/algorithms/{id}/templates` - Add code template

## Common Issues

### Issue: "ModuleNotFoundError"
**Solution:** Make sure virtual environment is activated
```bash
.venv/Scripts/activate  # Windows
```

### Issue: "could not connect to server"
**Solution:** Ensure PostgreSQL is running
```bash
# Windows (if installed as service)
services.msc → PostgreSQL → Start

# Mac
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Issue: "relation does not exist"
**Solution:** Run migrations
```bash
alembic upgrade head
```

### Issue: "Invalid authentication credentials"
**Solution:** Token expired (15 min), use refresh token or login again

## Database Configuration

Default connection (can be changed in `.env`):
```
postgresql+asyncpg://postgres:postgres@localhost:5432/algoref
```

### Custom Configuration
Create `.env` file in backend directory:
```env
POSTGRES_SERVER=localhost
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=algoref
POSTGRES_PORT=5432

# Optional: Override JWT secrets
SECRET_KEY=your_secret_key_here
REFRESH_SECRET_KEY=your_refresh_secret_key_here
```

## Development Tools

### Run Tests
```bash
pytest tests/
```

### Check Code Coverage
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### Format Code
```bash
black app/ tests/
isort app/ tests/
```

### Type Checking
```bash
mypy app/
```

## Project Structure
```
backend/
├── alembic/              # Database migrations
│   └── versions/         # Migration files
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/  # API route handlers
│   ├── core/             # Config, security, database
│   ├── models/           # SQLAlchemy models
│   └── schemas/          # Pydantic schemas
├── scripts/              # Utility scripts
│   └── create_admin.py
└── tests/
    └── integration/      # Integration tests
```

## Next Steps

1. **Add Algorithms:** Use Swagger UI or create via API
2. **Frontend Integration:** Connect frontend to http://localhost:8000
3. **Production Deploy:**
   - Change admin password
   - Update SECRET_KEY and REFRESH_SECRET_KEY
   - Use production database
   - Enable HTTPS
   - Add rate limiting

## Support

- **Documentation:** `PHASE2_IMPLEMENTATION_SUMMARY.md`
- **API Spec:** `../api-contract.yaml`
- **Phase 1 Report:** `PHASE1_COMPLETE.md`
