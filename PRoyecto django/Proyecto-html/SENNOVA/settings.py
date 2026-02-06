"""
⚙️ CONFIGURACIÓN PRINCIPAL DEL PROYECTO SENNOVA

Este archivo controla:
- Seguridad (claves secretas, hosts permitidos)
- Base de datos (SQLite)
- Aplicaciones instaladas (Gesicom, Usuarios, etc)
- Middleware (procesadores de solicitudes)
- Archivos estáticos (CSS, JS, imágenes)
- Email (SMTP para enviar mensajes)

Generado con Django 5.2.7
"""

from pathlib import Path
import os

# 📁 Define la carpeta raíz del proyecto (sube 2 niveles de directorios)
BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 SEGURIDAD: Configuración básica de desarrollo
# ⚠️ IMPORTANTE: Cambiar SECRET_KEY en producción por una variable de entorno
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-xjv@=pz08182&5z4y-5o*&!xl&na@yg#str+@u6--2&p_=&8s*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
🐛 DEBUG: Activa mensajes de error detallados (DESACTIVAR EN PRODUCCIÓN)
# 🌐 Lista de dominios/servidores que pueden acceder a la aplicación
# Se configura desde variables de entorno (ej: localhost,127.0.0.1,midominio.com)
_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()] if _hosts else []

📦 APLICACIONES INSTALADAS: Apps de Django + Apps del proyecto
# Application definition

INSTALLED_APPS = [
    # 🏢 Aplicaciones de Django
    'django.contrib.admin',              # Panel de administración
    'django.contrib.auth',               # Sistema de usuarios/autenticación
    'django.contrib.contenttypes',       # Gestión de tipos de contenido
    'django.contrib.sessions',           # Sesiones de usuarios
    'django.contrib.messages',           # Sistema de mensajes emergentes
    'django.contrib.staticfiles',        # Gestión de CSS, JS, imágenes
    
    # 🏃 Aplicaciones del proyecto SENNOVA
    'Gesicom',                           # App principal (gestión de evidencias)
    'Usuarios.apps.UsuariosConfig',      # App de login/registro
    'cuentas',                           # App de cuentas y recuperación de contraseña,
]

# 🔄 MIDDLEWARE: Procesadores de solicitudes HTTP (en orden de ejecución)
MIDDLEWARE = [      # Protección contra ataques
    'django.contrib.sessions.middleware.SessionMiddleware',  # Mantiene sesiones activas
    'django.middleware.common.CommonMiddleware',             # Procesamiento común
    'django.middleware.csrf.CsrfViewMiddleware',             # Protección contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Maneja usuario actual
    'django.contrib.messages.middleware.MessageMiddleware',   # Sistema de mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Previene clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔗 Archivo que contiene todas las rutas (URLs) del proyecto
ROOT_URLCONF = 'SENNOVA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SENNOVA.wsgi.application'


# 🗄️ BASE DE DATOS: SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Usa base de datos SQLite
        'NAME': BASE_DIR / 'db.sqlite3',         # Ubicación del archivo DB
    }
}


# 🔐 VALIDACIÓN DE CONTRASEÑAS: Reglas que deben cumplir las contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # No usar datos del usuario (nombre, email, etc) en la contraseña
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Mínimo 8 caracteres
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # No usar contraseñas comunes (123456, password, etc)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # No usar solo números
    },
    {
        'NAME': 'Gesicom.validators.EightCharUpperNumberOrSpecialValidator',
        # Personalizado: 8 caracteres, mayúscula, número o carácter especial


# 🌍 INTERNACIONALIZACIÓN: Idioma, zona horaria
LANGUAGE_CODE = 'en-us'  # Idioma predeterminado: inglés
TIME_ZONE = 'UTC'        # Zona horaria: UTC (Universal)
USE_I18N = True          # Activar soporte multiidioma
USE_TZ = True            # Usar zonas horarias en datetime


# 📦 ARCHIVOS ESTÁTICOS: CSS, JavaScript, imágenes
STATIC_URL = 'static/'  # URL donde se acceden los archivos estáticos

# Media (uploads de archivos de evidencias)
MEDIA_URL = '/media/'
ME📄 ARCHIVOS DE USUARIO: Descargas de evidencias, documentos, etc
MEDIA_URL = '/media/'                   # URL para acceder a los archivos
MEDIA_ROOT = BASE_DIR / 'media'         # Carpeta donde se guardan los archivosor variables de entorno)
# Si se define EMAIL_HOST_USER, usa SMTP; si no, usa backend de consola
if os.environ.get('EMAIL_HOST_USER'):
    # Usar servidor SMTP (Gmail, Outlook, Yahoo, etc)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')       # Email del remitente
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '') # Contraseña o token
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'  # Cifrado TLS
    EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True' # Cifrado SSL
    if EMAIL_USE_SSL:
        EMAIL_USE_TLS = False  # No usar TLS si usamos SSL
    
    # Detectar el dominio del email para autoconfigurar el servidor SMTP
    _domain = EMAIL_HOST_USER.split('@')[-1].lower() if '@' in EMAIL_HOST_USER else ''
    
    # 🔧 Configuración automática para proveedores populares
    _providers = {
        'gmail.com': ('smtp.gmail.com', 587, True, False),
        'outlook.com': ('smtp.office365.com', 587, True, False),
        'hotmail.com': ('smtp.office365.com', 587, True, False),
        'live.com': ('smtp.office365.com', 587, True, False),
        'yahoo.com': ('smtp.mail.yahoo.com', 587, True, False),
        'yahoo.es': ('smtp.mail.yahoo.com', 587, True, False),
        'icloud.com': ('smtp.mail.me.com', 587, True, False),
        'zoho.com': ('smtp.zoho.com', 587, True, False),
        # Si está configurado manualmente
        EMAIL_HOST = os.environ.get('EMAIL_HOST')
        EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    else:
        # Si NO: usar configuración automática según el proveedor
        _fallback = _providers.get(_domain, ('smtp.gmail.com', 587, True, False))
        EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL = _fallback
else:
    # Si NO hay EMAIL_HOST_USER: solo mostrar emails en consola (desarrollo)   EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    else:
        _fallback = _providers.get(_domain, ('smtp.gmail.com', 587, True, False))
        EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL = _fallback
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@gesicom.local')

# 🔐 REDIRECCIONES DE AUTENTICACIÓN
LOGIN_REDIRECT_URL = '/home/'    # Después de login: ir a home
LOGOUT_REDIRECT_URL = '/login/'  # Después de logout: ir a login

# 🔑 CAMPO ID POR DEFECTO: BigAutoField = números muy grandes (hasta 9 billones)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
