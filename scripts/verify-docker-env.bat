@echo off
REM Comprehensive Docker environment verification script (Windows)
REM Usage: scripts\verify-docker-env.bat

echo =========================================
echo Docker Environment Verification
echo =========================================
echo.

REM 1. Check Docker installation
echo 1. Checking Docker installation...
docker --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    docker --version
    echo [92m✅ Docker installed[0m
) else (
    echo [91m❌ Docker not installed[0m
    exit /b 1
)

docker-compose --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    docker-compose --version
    echo [92m✅ Docker Compose installed[0m
) else (
    echo [91m❌ Docker Compose not installed[0m
    exit /b 1
)
echo.

REM 2. Check .env file
echo 2. Checking .env file...
if exist ".env" (
    echo [92m✅ .env file exists[0m
    findstr /C:"SECRET_KEY=" .env >nul && (
        findstr /C:"SECRET_KEY=your-secret-key-here" .env >nul && (
            echo [93m⚠️  SECRET_KEY appears to be default value[0m
        ) || (
            echo [92m✅ SECRET_KEY is set (not default)[0m
        )
    )
    findstr /C:"DATABASE_URL=" .env >nul && (
        echo [92m✅ DATABASE_URL is set[0m
    ) || (
        echo [91m❌ DATABASE_URL not found in .env[0m
    )
) else (
    echo [91m❌ .env file missing - create from .env.example[0m
    exit /b 1
)
echo.

REM 3. Validate docker-compose.yml
echo 3. Validating docker-compose.yml...
docker-compose config >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ docker-compose.yml is valid[0m
) else (
    echo [91m❌ docker-compose.yml has syntax errors[0m
    docker-compose config
    exit /b 1
)
echo.

REM 4. Check for port conflicts
echo 4. Checking for port conflicts...
netstat -an | findstr ":5432" | findstr "LISTENING" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [93m⚠️  Port 5432 is already in use[0m
) else (
    echo [92m✅ Port 5432 is available[0m
)

netstat -an | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [93m⚠️  Port 8000 is already in use[0m
) else (
    echo [92m✅ Port 8000 is available[0m
)

netstat -an | findstr ":3000" | findstr "LISTENING" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [93m⚠️  Port 3000 is already in use[0m
) else (
    echo [92m✅ Port 3000 is available[0m
)
echo.

REM 5. Build Docker images
echo 5. Building Docker images...
echo ℹ️  This may take a few minutes on first run...
docker-compose build >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ Docker images built successfully[0m
) else (
    echo [91m❌ Docker build failed[0m
    exit /b 1
)
echo.

REM 6. Start services
echo 6. Starting Docker services...
echo ℹ️  Starting postgres, backend, frontend...
docker-compose up -d

echo Waiting for services to start (30 seconds)...
timeout /t 30 /nobreak >nul
echo.

REM 7. Check service health
echo 7. Checking service health...

REM PostgreSQL
docker-compose exec -T postgres pg_isready -U algoref_user >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ PostgreSQL is healthy[0m
) else (
    echo [91m❌ PostgreSQL is not healthy[0m
    docker-compose logs postgres
)

REM Backend (check if port is responding)
curl -s http://localhost:8000/docs >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ Backend is accessible (http://localhost:8000/docs)[0m
) else (
    echo [93m⚠️  Backend not yet accessible - may need more time[0m
)

REM Frontend
curl -s http://localhost:3000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ Frontend is accessible (http://localhost:3000)[0m
) else (
    echo [93m⚠️  Frontend not yet accessible - this may take longer to build[0m
)
echo.

REM 8. Test database connection
echo 8. Testing database connection...
docker-compose exec -T postgres psql -U algoref_user -d algoref -c "SELECT 1;" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ Database connection successful[0m
) else (
    echo [91m❌ Database connection failed[0m
)
echo.

REM 9. Check Alembic migrations
echo 9. Checking database migrations...
docker-compose exec -T backend alembic current 2>&1 | findstr "001" >nul
if %ERRORLEVEL% EQU 0 (
    echo [92m✅ Database migrations applied[0m
) else (
    echo [93m⚠️  No migrations detected - may need to run: docker-compose exec backend alembic upgrade head[0m
)
echo.

REM 10. Display running containers
echo 10. Container status:
docker-compose ps
echo.

REM 11. Summary
echo =========================================
echo Verification Summary
echo =========================================
echo [92m✅ Docker environment setup complete![0m
echo.
echo Access points:
echo   Backend API:  http://localhost:8000/docs
echo   Frontend:     http://localhost:3000
echo   PostgreSQL:   localhost:5432
echo.
echo Useful commands:
echo   View logs:    docker-compose logs -f [service]
echo   Stop all:     docker-compose down
echo   Restart:      docker-compose restart [service]
echo   Rebuild:      docker-compose up --build -d
echo   Clean slate:  docker-compose down -v
echo.
