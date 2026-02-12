# Docker Development Environment

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (for cloning repository)

### Setup Steps

1. **Clone repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd algo-reference
   ```

2. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Verify services are running**:
   ```bash
   docker-compose ps
   ```

5. **Access the application**:
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend: http://localhost:3000
   - PostgreSQL: localhost:5432

## Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network: algoref-network          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Frontend    │    │   Backend    │    │  PostgreSQL  │  │
│  │              │    │              │    │              │  │
│  │  React+Vite  │───▶│   FastAPI    │───▶│   Database   │  │
│  │  Port: 3000  │    │  Port: 8000  │    │  Port: 5432  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Available Commands

### Start Services
```bash
# Start all services in background
docker-compose up -d

# Start with logs visible
docker-compose up

# Start specific service
docker-compose up -d backend
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Stop Services
```bash
# Stop all services (keeps data)
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Rebuild Services
```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

### Execute Commands in Containers
```bash
# Backend: Run migrations
docker-compose exec backend alembic upgrade head

# Backend: Create admin user
docker-compose exec backend python scripts/create_admin.py

# Backend: Open Python shell
docker-compose exec backend python

# Backend: Run tests
docker-compose exec backend pytest

# Frontend: Install new package
docker-compose exec frontend npm install <package-name>

# PostgreSQL: Access database
docker-compose exec postgres psql -U algoref_user -d algoref
```

### Database Operations
```bash
# Create database backup
docker-compose exec postgres pg_dump -U algoref_user algoref > backup.sql

# Restore database backup
docker-compose exec -T postgres psql -U algoref_user algoref < backup.sql

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## Development Workflow

### Making Code Changes

**Backend (Python):**
1. Edit files in `backend/` directory
2. Uvicorn auto-reloads on file changes
3. Check logs: `docker-compose logs -f backend`

**Frontend (React):**
1. Edit files in `frontend/` directory
2. Vite HMR (Hot Module Replacement) applies changes instantly
3. Check logs: `docker-compose logs -f frontend`

**Database Schema Changes:**
1. Edit models in `backend/app/models/`
2. Create migration: `docker-compose exec backend alembic revision --autogenerate -m "description"`
3. Review migration in `backend/alembic/versions/`
4. Apply migration: `docker-compose exec backend alembic upgrade head`

### Troubleshooting

**Services won't start:**
```bash
# Check Docker is running
docker info

# Check service status
docker-compose ps

# View detailed errors
docker-compose logs
```

**Port already in use:**
```bash
# Find process using port
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Linux/Mac:
lsof -i :8000
lsof -i :3000

# Stop conflicting service or change ports in docker-compose.yml
```

**Database connection errors:**
```bash
# Ensure postgres is healthy
docker-compose ps postgres

# Check health status
docker inspect algoref-postgres --format='{{.State.Health.Status}}'

# Restart postgres
docker-compose restart postgres
```

**Module not found errors:**
```bash
# Backend: Rebuild container
docker-compose build backend
docker-compose up -d backend

# Frontend: Rebuild node_modules
docker-compose exec frontend npm ci
docker-compose restart frontend
```

**File permission issues (Linux):**
```bash
# Fix ownership
sudo chown -R $USER:$USER backend/ frontend/
```

## Environment Variables

### Backend Variables (in .env)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key (change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token lifetime (default: 15)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token lifetime (default: 7)
- `CORS_ORIGINS`: Allowed frontend origins

### Frontend Variables (in .env)
- `VITE_API_BASE_URL`: Backend API URL

## Performance Optimization

### Improving Build Speed
```yaml
# Use BuildKit for faster builds (add to docker-compose.yml)
COMPOSE_DOCKER_CLI_BUILD=1
DOCKER_BUILDKIT=1
```

### Volume Caching
- Frontend `node_modules` volume prevents re-install on restart
- PostgreSQL data volume persists between restarts

## Production Deployment

This Docker setup is for **development only**. For production:

1. Use multi-stage builds for smaller images
2. Don't mount source code as volumes
3. Use environment-specific configs
4. Enable HTTPS/SSL
5. Use managed database (not Docker PostgreSQL)
6. Implement proper secret management

See `docs/deployment-strategy.md` for production deployment guide.

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- Backend tests with PostgreSQL service
- Frontend tests and build
- Docker image build validation
- docker-compose config validation

## Health Checks

**PostgreSQL:**
- Health check: `pg_isready -U algoref_user -d algoref`
- Interval: 10s
- Timeout: 5s
- Retries: 5

**Backend:**
- Endpoint: `GET /health` (implement in FastAPI)
- Expected: 200 OK

**Frontend:**
- Dev server running on port 3000
- Should serve index.html

## Network Configuration

All services run on shared Docker network: `algoref-network`

Service-to-service communication uses container names:
- Frontend → Backend: `http://backend:8000`
- Backend → PostgreSQL: `postgres:5432`

External access uses localhost:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## Security Notes

**Development Environment:**
- Uses default passwords (NOT for production!)
- Exposes all ports to localhost
- No SSL/HTTPS
- DEBUG mode enabled

**Before Production:**
- [ ] Change all passwords and secrets
- [ ] Remove port exposures (use reverse proxy)
- [ ] Enable HTTPS
- [ ] Disable debug mode
- [ ] Review CORS configuration
- [ ] Enable rate limiting
- [ ] Scan images for vulnerabilities

## Support

For issues or questions:
1. Check `docker-compose logs -f`
2. Verify Docker Desktop is running
3. Check `docs/deployment-strategy.md`
4. Review GitHub Actions CI logs
5. Create GitHub issue with logs attached
