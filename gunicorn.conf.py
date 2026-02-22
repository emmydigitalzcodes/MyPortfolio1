# gunicorn.conf.py - Gunicorn configuration
import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = "gthread"
threads = int(os.environ.get('GUNICORN_THREADS', 4))
worker_connections = 1000

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'portfolio'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (handled by Railway)
forwarded_allow_ips = '*'
 secure_scheme_headers = {
     'X-FORWARDED-PROTOCOL': 'ssl',
     'X-FORWARDED-PROTO': 'https',
     'X-FORWARDED-SSL': 'on'
 }

# Performance
max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = 50
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 120))
keepalive = 5
graceful_timeout = 30

# Preload application for memory efficiency
preload_app = True