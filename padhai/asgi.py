"""
ASGI config for padhai project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "padhai.settings")
application = get_asgi_application()
