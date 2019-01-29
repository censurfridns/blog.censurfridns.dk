"""
WSGI config for blog_tyk_nu project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
application = get_wsgi_application()

