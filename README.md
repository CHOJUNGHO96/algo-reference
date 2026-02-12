# Algorithm Reference Learning Platform

Production-level coding interview algorithm reference platform that organizes algorithms by formula/pattern, not just problem-solving.

## 🎯 Project Vision

**Target Users**: Early-to-intermediate developers preparing for coding interviews who want to transition from rote memorization to structural understanding of algorithms.

**Unique Value Proposition**: This is a reference site that systematizes 'formula + thought process + application pattern + code template' — not just problem-solving practice.

## 🏗️ Architecture

### Tech Stack

**Backend**:
- FastAPI (Python 3.11+) - Modern async web framework
- PostgreSQL 15+ - Production database with full-text search
- SQLAlchemy 2.0 - Async ORM
- Pydantic v2 - Data validation
- JWT Authentication - Admin security

**Frontend**:
- React 18 + TypeScript - Modern UI framework
- Vite - Lightning-fast build tool
- Redux Toolkit + RTK Query - State management + API
- Ant Design - Professional UI components
- Prism.js - Syntax highlighting

**DevOps**:
- Docker + Docker Compose - Local development
- GitHub Actions - CI/CD
- Pytest + Jest - Testing
- Playwright - E2E testing

### Database Schema

**Core Tables**:
- `categories` - Algorithm categories (Two Pointer, Sliding Window, DP, etc.)
- `difficulty_levels` - Easy, Medium, Hard
- `programming_languages` - Python, C++, Java
- `algorithms` - Main content (8-point structure)
- `code_templates` - Language-specific code
- `users` - Admin authentication

### API Structure

**Public Endpoints**:
- `GET /api/v1/algorithms` - List with filters
- `GET /api/v1/algorithms/{slug}` - Detail view
- `GET /api/v1/categories` - Category tree
- `GET /api/v1/languages` - Available languages

**Admin Endpoints** (JWT Auth):
- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/admin/algorithms` - Create
- `PUT /api/v1/admin/algorithms/{id}` - Update
- `DELETE /api/v1/admin/algorithms/{id}` - Delete

See `api-contract.yaml` for complete OpenAPI specification.

## 📐 8-Point Content Structure

Each algorithm follows this systematic structure:

1. **Concept Summary** - One paragraph explanation
2. **Core Formulas/Patterns** - Key formulas with syntax highlighting
3. **Thought Process** - Step-by-step approach
4. **Application Conditions** - When to use / when NOT to use
5. **Time/Space Complexity** - Big-O notation in highlighted box
6. **Representative Problem Types** - Common problem patterns
7. **Code Templates** - Python, C++, Java tabs with copy button
8. **Common Mistakes** - Pitfall warnings

## 🎨 Design Philosophy

**Visual Identity**:
- Primary theme: Dark mode (GitHub Dark: #0d1117 base, #e6edf3 text)
- Light mode available as toggle
- Color-coded categories (Blue: Two Pointer, Purple: Sliding Window, etc.)
- Modern, developer-friendly design

**Layout Pattern**:
```
Desktop (3-column):
┌──────────────┬─────────────────────────────┬──────────┐
│ Sidebar Nav  │  Algorithm Cards Grid (3-4) │ Details  │
│ (240px)      │                             │ Sidebar  │
│              │  [Card] [Card] [Card]       │ (280px)  │
│ - Categories │  [Card] [Card] [Card]       │          │
│ - Search     │                             │          │
│ - Filters    │  Pagination                 │          │
└──────────────┴─────────────────────────────┴──────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Local Development Setup

1. **Clone and setup**:
```bash
git clone <repository-url>
cd algo-reference
cp .env.example .env  # Update with your configuration
```

2. **Start services with Docker Compose**:
```bash
docker-compose up -d
```

3. **Run database migrations**:
```bash
docker-compose exec backend alembic upgrade head
```

4. **Seed initial data**:
```bash
docker-compose exec backend python scripts/seed_data.py
```

5. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Development Workflow

**Backend development**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend development**:
```bash
cd frontend
npm install
npm run dev
```

**Run tests**:
```bash
# Backend tests
cd backend
pytest --cov=app

# Frontend tests
cd frontend
npm test

# E2E tests
cd tests/e2e
npx playwright test
```

## 👥 Team Structure

This project is being built using a parallel team approach with clear ownership:

| Role | Ownership | Primary Responsibilities |
|------|-----------|-------------------------|
| **Backend Architect** | `backend/` | FastAPI, SQLAlchemy, API endpoints, JWT auth |
| **Frontend Architect** | `frontend/` | React, TypeScript, Redux, UI components |
| **Content Generator** | `content-generator/` | AI-generated algorithm content, validation |
| **DevOps Specialist** | Docker, CI/CD | Infrastructure, deployment, monitoring |
| **QA Specialist** | `tests/` | Testing strategy, pytest, Jest, Playwright |
| **Team Lead** | Coordination | API contract, integration, deployment |

## 📊 Development Phases

### Phase 1: Foundation (Current - 3 hours)
- ✅ API contract specification (OpenAPI)
- 🔄 Backend project structure
- 🔄 Frontend project structure
- 🔄 Content generation preparation
- 🔄 Docker development environment
- 🔄 Testing infrastructure

### Phase 2: Core Implementation (5 hours)
- Backend CRUD endpoints
- Frontend algorithm listing & detail pages
- Admin CMS interface
- AI-generated content (15-20 algorithms)
- Database seeding
- Integration tests

### Phase 3: Integration & Deployment (4 hours)
- E2E testing
- Performance optimization
- Accessibility improvements
- Production deployment
- Monitoring setup
- Final QA

## 📝 Content Generation

Algorithms are AI-generated using structured prompts to ensure:
- Consistency across all entries
- Accurate code templates
- Real LeetCode problem references
- Common mistake identification

Target: 15-20 core algorithms covering:
- Two Pointer patterns
- Sliding Window techniques
- Binary Search variants
- DFS/BFS traversals
- Dynamic Programming (1D/2D)
- Greedy algorithms
- Union-Find
- Topological Sort
- And more...

## 🧪 Testing Strategy

**Coverage Targets**:
- Backend unit tests: ≥80%
- Frontend unit tests: ≥75%
- Integration tests: ≥75% of endpoints
- E2E tests: 100% of critical flows

**Quality Gates**:
- All tests must pass before merge
- No console errors in production builds
- API response time p95 <200ms
- Frontend LCP <2s
- Lighthouse score ≥90

## 🚀 Deployment

**Backend**: Railway / Render / Fly.io
**Frontend**: Vercel / Netlify
**Database**: Railway PostgreSQL / Supabase
**Monitoring**: Sentry for error tracking

## 📖 API Documentation

Interactive API documentation available at:
- Development: http://localhost:8000/docs
- Production: https://api.algoref.com/docs

## 🤝 Contributing

This is a production demonstration project. If you'd like to contribute:

1. Review the API contract (`api-contract.yaml`)
2. Check the 8-point content structure
3. Follow existing code patterns
4. Ensure tests pass and coverage maintained
5. Update documentation

## 📜 License

MIT License - See LICENSE file for details

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

**Built with**: FastAPI, React, TypeScript, PostgreSQL, Docker

**Purpose**: Demonstrating full-stack development best practices for algorithm learning platforms
