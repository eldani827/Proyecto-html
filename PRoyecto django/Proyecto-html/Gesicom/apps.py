from django.apps import AppConfig


class GesicomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GESICOM'

    def ready(self):
        # Import signals to ensure they are registered
        import GESICOM.signals
