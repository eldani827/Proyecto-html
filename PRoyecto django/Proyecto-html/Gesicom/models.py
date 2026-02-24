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
    user = models.O# d:\NUEVO PROYECTO\Proyecto-html\PRoyecto django\Proyecto-html\Gesicom\models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser de Django."""
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Sobreescribir el campo email como único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


# Perfil adicional para instructores. Apunta al usuario activo (`AUTH_USER_MODEL`).
class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Instructor: {self.user.get_full_name() or str(self.user)}"


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
# d:\NUEVO PROYECTO\Proyecto-html\PRoyecto django\Proyecto-html\Gesicom\models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    """Modelo que representa un rol en el sistema."""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser de Django."""
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Sobreescribir el campo email como único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


# Perfil adicional para instructores. Apunta al usuario activo (`AUTH_USER_MODEL`).
class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Instructor: {self.user.get_full_name() or str(self.user)}"


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
# En SENNOVA/settings.py - reemplazar estas líneas:

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'Gesicom.validators.SecurePasswordValidator',
    },
]

# Y también reemplazar:
AUTH_USER_MODEL = 'Gesicom.CustomUser'  # En lugar de 'auth.User'
# d:\NUEVO PROYECTO\Proyecto-html\PRoyecto django\Proyecto-html\Gesicom\validators.py
import re
from django.core.exceptions import ValidationError


class SecurePasswordValidator:
    """Validador de contraseñas seguras:
    
    Reglas:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número o carácter especial
    """

    def validate(self, password, user=None):
        if password is None:
            raise ValidationError("La contraseña es obligatoria.")

        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        # Al menos una mayúscula
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Debe contener al menos una letra mayúscula.")

        # Al menos una minúscula
        if not re.search(r"[a-z]", password):
            raise ValidationError("Debe contener al menos una letra minúscula.")

        # Al menos un número o carácter especial
        has_digit = re.search(r"\d", password) is not None
        has_special = re.search(r"[^A-Za-z0-9]", password) is not None
        if not (has_digit or has_special):
            raise ValidationError("Debe contener al menos un número o un carácter especial.")

    def get_help_text(self):
        return (
            "La contraseña debe tener al menos 8 caracteres, "
            "una mayúscula, una minúscula y un número o carácter especial."
        )


# Mantener el validador antiguo por compatibilidad
class EightCharUpperNumberOrSpecialValidator(SecurePasswordValidator):
    """Validador antiguo - hereda de SecurePasswordValidator para mantener compatibilidad"""
    pass
# d:\NUEVO PROYECTO\Proyecto-html\PRoyecto django\Proyecto-html\Usuarios\views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

ROLE_ROUTES = {
    'instructor': 'role_instructor',
    'investigador': 'role_investigador',
    'dinamizador': 'role_dinamizador',
    'coordinador': 'role_coordinador',
    'usuario': 'usuario',
}


def _validate_password(password1, password2=None):
    errors = []
    
    if not password1:
        errors.append('La contraseña es obligatoria.')
        return errors
    
    if password2 is not None and password1 != password2:
        errors.append('Las contraseñas no coinciden.')
    
    if len(password1) < 8:
        errors.append('La contraseña debe tener al menos 8 caracteres.')
    
    if not re.search(r'[A-Z]', password1):
        errors.append('La contraseña debe tener al menos una mayúscula.')
    
    if not re.search(r'[a-z]', password1):
        errors.append('La contraseña debe tener al menos una minúscula.')
    
    if not re.search(r'[\d\W]', password1):
        errors.append('La contraseña debe tener al menos un número o carácter especial.')
    
    return errors


def login_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        email = request.POST.get('email', '')  # Cambiado de username a email
        password = request.POST.get('password', '')
        
        # Autenticar usando email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.get_full_name() or user.email}!')
            
            if user.is_superuser:
                return redirect('admin:index')
            if user.groups.filter(name='administrador').exists():
                return redirect('admin_menu')
            
            if role:
                target = ROLE_ROUTES.get(role, 'home')
            else:
                target = (
                    'usuario'
                    if user.groups.filter(name='usuario').exists()
                    else 'home'
                )
            return redirect(target)
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos')
            return render(request, 'login.html', {
                'error': 'Correo electrónico o contraseña incorrectos',
                'role': role,
                'email': email,
            })
    return render(request, 'login.html', {'role': role})


def register_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not first_name:
            errors.append('El nombre es obligatorio.')
        if not last_name:
            errors.append('El apellido es obligatorio.')
        if not email:
            errors.append('El correo es obligatorio.')
        
        errors.extend(_validate_password(password1, password2))
        
        if User.objects.filter(email=email).exists():
            errors.append('Ese correo ya está registrado.')

        if errors:
            return render(request, 'register.html', {
                'errors': errors,
                'role': role,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

        # Crear usuario con CustomUser - usar email como username
        username = email  # Usamos el email como username para mantener compatibilidad
        user = User.objects.create_user(
            username=username,
            email=email, 
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Asignar grupo por defecto
        g, _ = Group.objects.get_or_create(name='usuario')
        user.groups.add(g)
        
        messages.success(request, '¡Cuenta creada exitosamente!')
        login(request, user)
        target = ROLE_ROUTES.get(role, 'usuario')
        return redirect(target)

    return render(request, 'register.html', {'role': role})
    OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
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