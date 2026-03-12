"""
⚡ ASGI: Interfaz de Servidor para aplicaciones async (Uvicorn, Hypercorn, etc)

ASGI permite conexiones en tiempo real:
- WebSockets
- Streaming de datos
- Conexiones keep-alive

Se usa en servidores modernos para aplicaciones de tiempo real.
"""
import os
from django.core.asgi import get_asgi_application

# Define qué archivo de configuración usar (settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SENNOVA.settings')

# Crea la aplicación ASGI
application = get_asgi_application()
