@echo off
REM Development environment setup script for Windows

echo.
echo ========================================
echo  Algorithm Reference Platform Setup
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Check if .env exists
if not exist .env (
    echo.
    echo [INFO] Creating .env file from template...
    copy .env.example .env >nul
    echo [OK] .env file created
    echo [WARNING] Please update .env with your configuration
) else (
    echo [OK] .env file already exists
)

echo.
echo [INFO] Building Docker containers...
docker-compose build
if errorlevel 1 (
    echo [ERROR] Docker build failed
    pause
    exit /b 1
)

echo.
echo [INFO] Starting services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)

echo.
echo [INFO] Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul

echo.
echo [INFO] Running database migrations...
docker-compose exec backend alembic upgrade head
if errorlevel 1 (
    echo [WARNING] Migration failed - database may not be ready yet
)

echo.
echo ========================================
echo  Development environment ready!
echo ========================================
echo.
echo Services running at:
echo   - Backend API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Frontend: http://localhost:3000
echo   - PostgreSQL: localhost:5432
echo.
echo Useful commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Restart: docker-compose restart
echo.
pause
