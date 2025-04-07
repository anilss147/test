"""
WSGI config for clothing_store project.
"""

import os

from django.core.wsgi import get_wsgi_application

# Check if we're running on production (e.g., Render)
if os.environ.get('RENDER') or os.environ.get('PRODUCTION'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings_prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')

application = get_wsgi_application()
