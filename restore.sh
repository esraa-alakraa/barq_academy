#!/usr/bin/env bash
set -e

BACKUP_DIR="./backups"
LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/pg_backup_*.sql 2>/dev/null | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "[!] Error: No backup files found in $BACKUP_DIR"
    exit 1
fi

echo "[*] Restoring database from: $LATEST_BACKUP"

docker compose exec -T postgres psql -U barq_app -d postgres -c "DROP DATABASE IF EXISTS barq_tasks;"
docker compose exec -T postgres psql -U barq_app -d postgres -c "CREATE DATABASE barq_tasks;"
docker compose exec -T postgres psql -U barq_app -d barq_tasks < "$LATEST_BACKUP"

echo "[✓] Database restored successfully from $LATEST_BACKUP"