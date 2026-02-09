from django.db import models


# Modelo que representa datos personales básicos (persona de contacto)
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    contraseña = models.CharField(max_length=8)  # ATENCIÓN: campo en texto plano (mejor usar User)


# Modelo que describe un rol asociado a una persona
class Roles(models.Model):
    Rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    Persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return self.Rol


# Modelo alternativo para usuarios; considerar usar el modelo de Django en su lugar
class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)  # ATENCIÓN: mejor usar sistema de usuarios de Django
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario


# Clase para almacenar a los usuarios con rol de instructor (estructura similar a Persona)
class Instructor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    contraseña = models.CharField(max_length=8)  # ATENCIÓN: ver nota de seguridad arriba
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


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

