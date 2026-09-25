#!/usr/bin/env bash
set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/pg_backup_$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"

echo "[*] Starting PostgreSQL backup..."
docker compose exec -T postgres pg_dump -U barq_app -d barq_tasks > "$BACKUP_FILE"

echo "[✓] Backup completed successfully: $BACKUP_FILE"