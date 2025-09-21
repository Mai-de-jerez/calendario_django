"""
WSGI config for calendary project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys


path = '/home/May1985/calendario_django'
if path not in sys.path:
    sys.path.append(path)

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendary.settings')

# Importa la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
