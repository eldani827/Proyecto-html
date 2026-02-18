from django.db import models
from django.conf import settings


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# Perfil adicional para instructores. Apunta al usuario activo (`AUTH_USER_MODEL`).
class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # `get_full_name` existe en `auth.User`
        return f"Instructor: {getattr(self.user, 'get_full_name')() if hasattr(self.user, 'get_full_name') else str(self.user)}"


class Envio(models.Model):
    PROYECTO_CHOICES = [
        ("LEM", "LEM"),
        ("GIVIT", "GIVIT"),
        ("ACAF", "ACAF"),
        ("DEPOS", "DEPOS"),
        ("IFPI", "IFPI"),
        ("TUGA", "TUGA"),
    ]
    nombre = models.CharField(max_length=80, blank=True)
    proyecto = models.CharField(max_length=20, choices=PROYECTO_CHOICES, blank=True)
    tipo_evidencia = models.CharField(max_length=50)
    link_evidencia = models.URLField(max_length=200, blank=True, null=True)
    archivo_evidencia = models.FileField(upload_to='evidencias/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_envio = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='envios')

    class Meta:
        ordering = ['-fecha_envio']

    def __str__(self):
        return self.tipo_evidencia