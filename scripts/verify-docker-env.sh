#!/bin/bash
# Comprehensive Docker environment verification script
# Usage: ./scripts/verify-docker-env.sh

set -e  # Exit on error

echo "========================================="
echo "Docker Environment Verification"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "ℹ️  $1"
}

# 1. Check Docker installation
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    success "Docker installed: $DOCKER_VERSION"
else
    error "Docker not installed"
    exit 1
fi

if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    success "Docker Compose installed: $COMPOSE_VERSION"
else
    error "Docker Compose not installed"
    exit 1
fi
echo ""

# 2. Check .env file
echo "2. Checking .env file..."
if [ -f ".env" ]; then
    success ".env file exists"

    # Check required variables
    if grep -q "SECRET_KEY=" .env && ! grep -q "SECRET_KEY=your-secret-key-here" .env; then
        success "SECRET_KEY is set (not default)"
    else
        warning "SECRET_KEY appears to be default value"
    fi

    if grep -q "DATABASE_URL=" .env; then
        success "DATABASE_URL is set"
    else
        error "DATABASE_URL not found in .env"
    fi
else
    error ".env file missing - create from .env.example"
    exit 1
fi
echo ""

# 3. Validate docker-compose.yml
echo "3. Validating docker-compose.yml..."
if docker-compose config > /dev/null 2>&1; then
    success "docker-compose.yml is valid"
else
    error "docker-compose.yml has syntax errors"
    docker-compose config
    exit 1
fi
echo ""

# 4. Check for port conflicts
echo "4. Checking for port conflicts..."
PORTS=(5432 8000 3000)
CONFLICTS=0

for PORT in "${PORTS[@]}"; do
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an 2>/dev/null | grep ":$PORT " | grep LISTEN > /dev/null; then
        warning "Port $PORT is already in use"
        CONFLICTS=$((CONFLICTS + 1))
    else
        success "Port $PORT is available"
    fi
done

if [ $CONFLICTS -gt 0 ]; then
    warning "$CONFLICTS port(s) in use - may cause conflicts"
fi
echo ""

# 5. Build Docker images
echo "5. Building Docker images..."
info "This may take a few minutes on first run..."

if docker-compose build --quiet 2>&1; then
    success "Docker images built successfully"
else
    error "Docker build failed"
    exit 1
fi
echo ""

# 6. Start services
echo "6. Starting Docker services..."
info "Starting postgres, backend, frontend..."

docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services to start (max 60s)..."
SECONDS=0
MAX_WAIT=60

while [ $SECONDS -lt $MAX_WAIT ]; do
    if docker-compose ps | grep -q "Up.*healthy"; then
        break
    fi
    sleep 2
    echo -n "."
done
echo ""

if [ $SECONDS -ge $MAX_WAIT ]; then
    warning "Services took longer than expected to start"
fi

sleep 5  # Give services extra time to fully initialize
echo ""

# 7. Check service health
echo "7. Checking service health..."

# PostgreSQL
if docker-compose exec -T postgres pg_isready -U algoref_user > /dev/null 2>&1; then
    success "PostgreSQL is healthy"
else
    error "PostgreSQL is not healthy"
    docker-compose logs postgres | tail -20
fi

# Backend
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    success "Backend is accessible (http://localhost:8000/docs)"
else
    warning "Backend not yet accessible - checking logs..."
    docker-compose logs backend | tail -20
fi

# Frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    success "Frontend is accessible (http://localhost:3000)"
else
    warning "Frontend not yet accessible - this may take longer to build"
    docker-compose logs frontend | tail -20
fi
echo ""

# 8. Test database connection
echo "8. Testing database connection..."
if docker-compose exec -T postgres psql -U algoref_user -d algoref -c "SELECT 1;" > /dev/null 2>&1; then
    success "Database connection successful"
else
    error "Database connection failed"
fi
echo ""

# 9. Check Alembic migrations
echo "9. Checking database migrations..."
MIGRATION_OUTPUT=$(docker-compose exec -T backend alembic current 2>&1 || echo "")

if echo "$MIGRATION_OUTPUT" | grep -q "001"; then
    success "Database migrations applied"
else
    warning "No migrations detected - may need to run: docker-compose exec backend alembic upgrade head"
fi
echo ""

# 10. Display running containers
echo "10. Container status:"
docker-compose ps
echo ""

# 11. Summary
echo "========================================="
echo "Verification Summary"
echo "========================================="
success "Docker environment setup complete!"
echo ""
echo "Access points:"
echo "  Backend API:  http://localhost:8000/docs"
echo "  Frontend:     http://localhost:3000"
echo "  PostgreSQL:   localhost:5432"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose logs -f [service]"
echo "  Stop all:     docker-compose down"
echo "  Restart:      docker-compose restart [service]"
echo "  Rebuild:      docker-compose up --build -d"
echo "  Clean slate:  docker-compose down -v"
echo ""
