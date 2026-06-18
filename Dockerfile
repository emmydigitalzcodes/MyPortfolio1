# ============================================
# Django Portfolio - Production Dockerfile
# Optimized for Railway Deployment
# ============================================

# Use official Python image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    SECRET_KEY=dummy-build-key \
    DJANGO_SETTINGS_MODULE=portfolio.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create directories for media, static files and logs
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files using dummy key (real key injected at runtime)
RUN SECRET_KEY=dummy-build-key python manage.py collectstatic --noinput
RUN DJANGO_DEBUG=True SECRET_KEY=dummy-build-key python manage.py collectstatic --noinput --ignore=*.scss --ignore=select2/i18n/*.js

# Create non-root user for security
RUN useradd -m -u 1000 django && \
    chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health/ || exit 1

# Start command
CMD sh -c "python manage.py migrate --noinput && \
    gunicorn portfolio.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -"