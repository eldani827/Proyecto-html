"""Configuración de la app 'Gesicom'.

La función ready() importa las señales para que se conecten al arrancar
la aplicación y garantizar la creación/gestión de grupos y asignaciones.
"""
from django.apps import AppConfig


class GesicomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gesicom'

    def ready(self):
        # Importar señales aquí para que se registren cuando la app arranca
        from . import signals  # noqa
