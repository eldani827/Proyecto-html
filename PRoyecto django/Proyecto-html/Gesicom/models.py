from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser de Django."""
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos adicionales de perfil
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    
    # Sobreescribir el campo email como único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modelo para almacenar información adicional de instructores
class InstructorProfile(models.Model):
    """Perfil adicional para instructores."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Instructor: {self.user.get_full_name()}"


# Modelo que representa un envío de evidencia (link o archivo)
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

    def __str__(self):
        return self.tipo_evidencia

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser de Django."""
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos adicionales de perfil
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    
    # Sobreescribir el campo email como único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modelo para almacenar información adicional de instructores
class InstructorProfile(models.Model):
    """Perfil adicional para instructores."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Instructor: {self.user.get_full_name()}"


# Modelo que representa un envío de evidencia (link o archivo)
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

    def __str__(self):
        return self.tipo_evidencia

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser de Django."""
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos adicionales de perfil
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    
    # Sobreescribir el campo email como único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modelo para almacenar información adicional de instructores
class InstructorProfile(models.Model):
    """Perfil adicional para instructores."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Instructor: {self.user.get_full_name()}"


# Modelo que representa un envío de evidencia (link o archivo)
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

    def __str__(self):
        return self.tipo_evidencia

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser de Django."""
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos adicionales de perfil
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    
    # Sobreescribir el campo email como único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modelo para almacenar información adicional de instructores
class InstructorProfile(models.Model):
    """Perfil adicional para instructores."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Instructor: {self.user.get_full_name()}"


# Modelo que representa un envío de evidencia (link o archivo)
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

    def __str__(self):
        return self.tipo_evidencia