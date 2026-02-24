"""Modelos para la aplicación Gesicom.

Se definen los modelos principales: `Rol`, `CustomUser`, `InstructorProfile` y `Envio`.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class CustomUser(AbstractUser):
    """Usuario personalizado que extiende `AbstractUser`.

    Se usa `email` como `USERNAME_FIELD` para autenticación por correo.
    """
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Evitar colisión de reverse accessors con el modelo auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        return self.email

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class InstructorProfile(models.Model):
    """Perfil adicional para instructores."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        full = getattr(self.user, 'get_full_name', None)
        if callable(full):
            name = full() or str(self.user)
        else:
            name = str(self.user)
        return f"Instructor: {name}"


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
        verbose_name = 'Envío de Evidencia'
        verbose_name_plural = 'Envíos de Evidencias'

    def __str__(self):
        return f"{self.tipo_evidencia} - {self.proyecto}"