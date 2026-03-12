"""
🔗 CONFIGURACIÓN DE RUTAS (URLs) DEL PROYECTO SENNOVA

Este archivo mapea URLs a funciones/vistas:
- /login/ → Página de inicio de sesión
- /register/ → Página de registro
- /home/ → Página principal
- /roles/instructor/ → Panel de instructor
- /admin/ → Panel de administración

Las rutas definen qué se muestra al acceder a cada URL.
"""
from django.contrib import admin                           # Panel admin
from django.urls import path                               # Definir rutas
from django.contrib.auth import views as auth_views       # Vistas de recuperación contraseña
from django.conf import settings                           # Configuración del proyecto
from django.conf.urls.static import static                # Servir archivos media
from Gesicom import views as gesicom_views                # Vistas principales
from Usuarios import views as usuarios_views              # Vistas de login/registro
from cuentas import views as cuentas_views                # Vistas de recuperación

urlpatterns = [
    path('admin/', admin.site.urls),                                 # 🏢 Panel de administración
    path('', usuarios_views.login_view, name='login_root'),         # 🏠 Inicio → redirige a login
    path('login/', usuarios_views.login_view, name='login'),        # 🔓 Página de login
    path('register/', usuarios_views.register_view, name='register'), # 📝 Página de registro
    path('home/', gesicom_views.home, name='home'),                 # 🏠 Página principal
    path('usuario/', gesicom_views.role_usuario, name='usuario'),   # 👤 Panel de usuario
    path('nosotros/', gesicom_views.nosotros, name='nosotros'),     # ℹ️ Página nosotros
    path('contacto/', gesicom_views.contacto, name='contacto'),     # 📞 Página contacto
    path('ayuda/', gesicom_views.ayuda, name='ayuda'),              # ❓ Página de ayuda
    path('portal/', gesicom_views.portal, name='portal'),           # 🚪 Portal
    
    # 👥 RUTAS POR ROLES (diferentes paneles según el rol del usuario)
    path('roles/instructor/', gesicom_views.role_instructor, name='role_instructor'),
    path('roles/instructor-table/', gesicom_views.instructor_table, name='instructor_table'),
    path('roles/investigador/', gesicom_views.role_investigador, name='role_investigador'),
    path('roles/dinamizador/', gesicom_views.role_dinamizador, name='role_dinamizador'),
    path('roles/coordinador/', gesicom_views.role_coordinador, name='role_coordinador'),
    path('access-denied/', gesicom_views.access_denied, name='access_denied'),  # 🚫 Acceso denegado
    
    # Panel de administración
    path('administracion/', gesicom_views.admin_menu, name='admin_menu'),
    path('proyecciones/', gesicom_views.proyecciones, name='proyecciones'),
    path('reportes/', gesicom_views.reportes, name='reportes'),
    path('reportes.csv', gesicom_views.reportes_csv, name='reportes_csv'),
    
    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Registro/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Registro/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Registro/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Registro/password_reset_complete.html'), name='password_reset_complete'),
    
    # recuperación con código
    path('olvide-password/', cuentas_views.olvide_password, name='olvide_password'),
    path('verificar-codigo/', cuentas_views.verificar_codigo, name='verificar_codigo'),
    path('restablecer-password/', cuentas_views.restablecer_password, name='restablecer_password'),
    
]

# 🖼️ Servir archivos media (imágenes, PDFs, etc) solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
