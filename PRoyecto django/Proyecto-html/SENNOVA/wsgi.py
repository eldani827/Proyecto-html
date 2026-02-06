"""
🚀 WSGI: Interfaz de Servidor Web (Gunicorn, uWSGI, etc)

WSGI es el estándar para aplicaciones web Python:
- Compatible con Gunicorn (producción)
- Compatible con Apache + mod_wsgi
- Requisito para desplegar en servidores

Se usa en servidores de producción.
"""
import os
from django.core.wsgi import get_wsgi_application

# Define qué archivo de configuración usar (settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SENNOVA.settings')

# Crea la aplicación WSGI
application = get_wsgi_application()
