@echo off
REM Backup PostgreSQL database from Docker container
REM Usage: scripts\backup-db.bat

set BACKUP_DIR=backups
set TIMESTAMP=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_FILE=%BACKUP_DIR%\algoref_backup_%TIMESTAMP%.sql

REM Create backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo Starting database backup...
echo Backup file: %BACKUP_FILE%

REM Dump database from Docker container
docker-compose exec -T postgres pg_dump -U algoref_user algoref > "%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Database backup completed successfully
    echo Backup saved to: %BACKUP_FILE%
    dir "%BACKUP_FILE%" | find "algoref_backup"
) else (
    echo ❌ Database backup failed
    exit /b 1
)
