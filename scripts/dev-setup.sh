#!/bin/bash
# Development environment setup script

echo "🚀 Setting up Algorithm Reference Platform development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Copy environment template if .env doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Build and start services
echo "🐳 Building Docker containers..."
docker-compose build

echo "🎬 Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec backend alembic upgrade head

# Create admin user
echo "👤 Creating admin user..."
docker-compose exec backend python scripts/create_admin.py

echo "✅ Development environment ready!"
echo ""
echo "Services running at:"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Frontend: http://localhost:3000"
echo "  - PostgreSQL: localhost:5432"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
