#!/bin/bash
set -e

echo "Waiting for postgres..."
while ! python -c "
import os
import sys
try:
    import psycopg2
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/construction_ai'))
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
  sleep 2
done

echo "Postgres ready. Running migrations..."
export FLASK_APP=app
flask db upgrade 2>/dev/null || true

echo "Starting application..."
exec "$@"
