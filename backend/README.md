# Algorithm Reference Platform - Backend API

FastAPI backend with PostgreSQL database, JWT authentication, and async SQLAlchemy 2.0.

## Tech Stack

- **FastAPI** 0.109+ - Modern async web framework
- **SQLAlchemy** 2.0+ - Async ORM with PostgreSQL
- **Pydantic** 2.5+ - Data validation and settings
- **PostgreSQL** - Primary database with full-text search
- **JWT** - Token-based authentication for admin CMS
- **Alembic** - Database migrations

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file (will be handled by DevOps):

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=algoref
POSTGRES_PORT=5432

SECRET_KEY=your-secret-key-here
REFRESH_SECRET_KEY=your-refresh-key-here
```

### 3. Run Database Migrations

```bash
# Create initial migration (after DevOps sets up PostgreSQL)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 4. Start Development Server

```bash
uvicorn app.main:app --reload
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── config.py        # Settings and configuration
│   │   ├── database.py      # Async SQLAlchemy session
│   │   └── security.py      # JWT and password utilities
│   ├── models/              # SQLAlchemy models
│   │   ├── algorithm.py     # Algorithm with 8-point content
│   │   ├── category.py      # Hierarchical categories
│   │   ├── code_template.py # Code implementations
│   │   ├── difficulty.py    # Difficulty levels
│   │   ├── language.py      # Programming languages
│   │   └── user.py          # Admin users
│   ├── schemas/             # Pydantic schemas
│   │   ├── algorithm.py
│   │   ├── category.py
│   │   ├── code_template.py
│   │   └── auth.py
│   └── api/
│       └── v1/
│           ├── endpoints/
│           │   ├── algorithms.py  # Public + Admin endpoints
│           │   ├── categories.py
│           │   ├── languages.py
│           │   └── auth.py
│           └── dependencies.py    # JWT middleware
├── alembic/                 # Database migrations
├── requirements.txt
└── alembic.ini
```

## API Endpoints

### Public Endpoints

- `GET /api/v1/algorithms` - List algorithms (paginated, filtered)
- `GET /api/v1/algorithms/{slug}` - Get algorithm details
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/categories/{slug}` - Get category details
- `GET /api/v1/languages` - List programming languages

### Admin Endpoints (JWT Required)

- `POST /api/v1/admin/algorithms` - Create algorithm
- `PUT /api/v1/admin/algorithms/{id}` - Update algorithm
- `DELETE /api/v1/admin/algorithms/{id}` - Delete algorithm
- `POST /api/v1/admin/algorithms/{id}/templates` - Add code template

### Authentication

- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

## Database Schema

### Categories
- Hierarchical category system with parent-child relationships
- Custom color coding for UI

### Algorithms
- 8-point content structure:
  1. **concept_summary** - High-level overview
  2. **core_formulas** - Key patterns/formulas (JSONB)
  3. **thought_process** - Step-by-step approach
  4. **application_conditions** - When to use/not use (JSONB)
  5. **time_complexity** - Big-O time complexity
  6. **space_complexity** - Big-O space complexity
  7. **problem_types** - Problem categories with LeetCode examples (JSONB)
  8. **common_mistakes** - Pitfalls to avoid

### Code Templates
- Multi-language code implementations
- Prism.js compatible syntax highlighting

### Full-text Search
- PostgreSQL `tsvector` on algorithm content
- Supports search across title, concept, and formulas

## Development Status

**Phase 1** ✅ - Foundation Complete:
- [x] Project structure
- [x] Database models (async SQLAlchemy 2.0)
- [x] Pydantic schemas matching OpenAPI spec
- [x] API route stubs
- [x] JWT authentication middleware
- [x] Alembic configuration

**Phase 2** - Implementation (Next):
- [ ] CRUD operations for all endpoints
- [ ] Full-text search implementation
- [ ] Database seed data
- [ ] Admin user creation
- [ ] Input validation and error handling

## Notes

- All endpoints are stubs returning mock data or 501 errors
- Database queries will be implemented in Phase 2
- JWT middleware is configured but user authentication is stubbed
- Alembic migrations need to be generated after PostgreSQL setup
