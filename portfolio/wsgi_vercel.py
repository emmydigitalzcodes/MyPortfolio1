"""
WSGI config for Vercel deployment.
"""

import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# For Vercel, export the application as 'app'
app = application