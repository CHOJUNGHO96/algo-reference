#!/bin/bash
# Backup PostgreSQL database from Docker container
# Usage: ./scripts/backup-db.sh

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/algoref_backup_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."
echo "Backup file: $BACKUP_FILE"

# Dump database from Docker container
docker-compose exec -T postgres pg_dump -U algoref_user algoref > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Database backup completed successfully"
    echo "Backup saved to: $BACKUP_FILE"

    # Display backup file size
    FILESIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Backup size: $FILESIZE"
else
    echo "❌ Database backup failed"
    exit 1
fi
