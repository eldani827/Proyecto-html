from django.db import models

# Create your models here

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    contraseña= models.CharField(max_length=8)

class Roles(models.Model):
    Rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    Persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    def __str__(self):
        return self.Rol
    

class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    def __str__(self):
        return self.usuario
    
# Clase para almacenar información sobre los usuarios del sistema.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    contraseña= models.CharField(max_length=8)
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    def __str__(self):
        return self.usuario

# Clase para almacenar información sobre los roles de los usuarios del sistema.

class Rol(models.Model):
    Rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return self.Rol

# Clase para almacenar a los usuarios con el rol de instructor en el sistema 

class Instructor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    contraseña= models.CharField(max_length=8)
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    def __str__(self):
        return self.usuario
    
class Envio(models.Model):
    tipo_evidencia = models.CharField(max_length=50)
    link_evidencia = models.URLField(max_length=200)
    archivo_evidencia = models.FileField(upload_to='evidencias/')
    fecha_envio = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.tipo_evidencia





