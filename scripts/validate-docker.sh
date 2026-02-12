#!/bin/bash
# Docker environment validation script

echo "🔍 Validating Docker Development Environment..."
echo ""

FAILED=0

# Test 1: Docker is running
echo "1️⃣  Checking Docker daemon..."
if docker info > /dev/null 2>&1; then
    echo "   ✅ Docker is running"
else
    echo "   ❌ Docker is not running"
    FAILED=$((FAILED + 1))
fi

# Test 2: docker-compose.yml is valid
echo "2️⃣  Validating docker-compose.yml..."
if docker-compose config > /dev/null 2>&1; then
    echo "   ✅ docker-compose.yml is valid"
else
    echo "   ❌ docker-compose.yml is invalid"
    FAILED=$((FAILED + 1))
fi

# Test 3: Required files exist
echo "3️⃣  Checking required files..."
FILES=(
    "backend/Dockerfile"
    "backend/.dockerignore"
    "frontend/Dockerfile"
    "frontend/.dockerignore"
    "docker-compose.yml"
    ".env.example"
    ".github/workflows/ci.yml"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file exists"
    else
        echo "   ❌ $file missing"
        FAILED=$((FAILED + 1))
    fi
done

# Test 4: Services can be built
echo "4️⃣  Testing Docker image builds..."
if docker-compose build --quiet > /dev/null 2>&1; then
    echo "   ✅ All images build successfully"
else
    echo "   ❌ Image build failed"
    FAILED=$((FAILED + 1))
fi

# Test 5: Services can start
echo "5️⃣  Testing service startup..."
if docker-compose up -d > /dev/null 2>&1; then
    echo "   ✅ Services started"

    # Wait for health checks
    echo "   ⏳ Waiting for health checks..."
    sleep 10

    # Test 6: PostgreSQL is healthy
    echo "6️⃣  Checking PostgreSQL health..."
    if docker-compose exec -T postgres pg_isready -U algoref_user -d algoref > /dev/null 2>&1; then
        echo "   ✅ PostgreSQL is healthy"
    else
        echo "   ❌ PostgreSQL is not healthy"
        FAILED=$((FAILED + 1))
    fi

    # Test 7: Backend is accessible
    echo "7️⃣  Checking Backend API..."
    sleep 5  # Give backend time to start
    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        echo "   ✅ Backend API is accessible"
    else
        echo "   ❌ Backend API is not accessible"
        FAILED=$((FAILED + 1))
    fi

    # Test 8: Frontend is accessible
    echo "8️⃣  Checking Frontend dev server..."
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        echo "   ✅ Frontend is accessible"
    else
        echo "   ❌ Frontend is not accessible"
        FAILED=$((FAILED + 1))
    fi

    # Test 9: Inter-service communication
    echo "9️⃣  Testing service communication..."
    if docker-compose exec -T backend python -c "import asyncpg; print('OK')" > /dev/null 2>&1; then
        echo "   ✅ Backend can communicate with PostgreSQL"
    else
        echo "   ❌ Backend cannot communicate with PostgreSQL"
        FAILED=$((FAILED + 1))
    fi

    # Cleanup
    echo ""
    echo "🧹 Cleaning up test environment..."
    docker-compose down -v > /dev/null 2>&1

else
    echo "   ❌ Services failed to start"
    FAILED=$((FAILED + 1))
fi

# Summary
echo ""
echo "========================================"
if [ $FAILED -eq 0 ]; then
    echo "✅ All validation tests passed!"
    echo "========================================"
    echo ""
    echo "Your Docker environment is ready for development."
    echo "Run 'docker-compose up -d' to start services."
    exit 0
else
    echo "❌ $FAILED validation test(s) failed"
    echo "========================================"
    echo ""
    echo "Please review the errors above and fix the issues."
    echo "Check docker-compose logs for more details."
    exit 1
fi
