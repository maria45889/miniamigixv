"""
ASGI config for miniamigixv project.

It exposes the ASGI callable as a module-level variable named `application`.
"""

import os
from django.core.asgi import get_asgi_application

# 🔐 Configuración del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniamigixv.settings')

# 🚀 Aplicación ASGI
application = get_asgi_application()

