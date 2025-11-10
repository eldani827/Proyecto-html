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
    


