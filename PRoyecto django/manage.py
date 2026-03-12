#!/usr/bin/env python
"""Script para ejecutar comandos administrativos de Django (ej. runserver, migrate)."""
import os
import sys


def main():
    """Configura Django y ejecuta el comando indicado en la línea de comandos."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SENNOVA.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y activado el entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
