"""Modelos de la app `cuentas`.

Recomendación: para almacenar códigos de recuperación usa un modelo con
campo de expiración en lugar de mantenerlos en memoria. Esto permite
persistencia, auditoría y escalabilidad.

Ejemplo (comentado):

# class RecoveryCode(models.Model):
#     email = models.EmailField()
#     code = models.IntegerField()
#     expires_at = models.DateTimeField()
#     used = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

"""
from django.db import models

# Define aquí los modelos de datos de la app (por ejemplo, códigos de recuperación o registros relacionados).
