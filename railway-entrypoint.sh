#!/bin/bash
# railway-entrypoint.sh - Entrypoint script for Railway

set -e

echo "🚀 Starting Django Portfolio on Railway..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
python -c "
import socket
import time
import os
import sys

host = os.environ.get('DATABASE_HOST', 'localhost')
port = int(os.environ.get('DATABASE_PORT', '5432'))

for i in range(30):
    try:
        socket.create_connection((host, port), timeout=5)
        print('✅ Database is ready!')
        sys.exit(0)
    except socket.error:
        print(f'Attempt {i+1}/30: Database not ready yet...')
        time.sleep(2)

print('❌ Database connection timeout')
sys.exit(1)
"

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Create cache table if using database cache
echo "🔄 Creating cache table..."
python manage.py createcachetable 2>/dev/null || true

# Collect static files (in case they weren't collected during build)
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Compress static files if django-compressor is installed
echo "🗜️  Compressing static files..."
python manage.py compress --force 2>/dev/null || true

echo "✅ Setup complete! Starting Gunicorn..."

# Start Gunicorn with Railway's PORT
exec gunicorn portfolio.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --worker-class gthread \
    --threads ${GUNICORN_THREADS:-4} \
    --worker-tmp-dir /dev/shm \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --keep-alive 5 \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance \
    --preload