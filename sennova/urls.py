"""
URL configuration for sennova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from Gesicom import views as gesicom_views
from Usuarios import views as usuarios_views
from cuentas import views as cuentas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador/', include(('admin_personalizado.urls', 'admin_personalizado'), namespace='admin_personalizado')),
    path('', RedirectView.as_view(pattern_name='admin_personalizado:dashboard', permanent=False)),
    
    # 🔓 Página de login y registro de compañeros
    path('login/', usuarios_views.login_view, name='login'),
    path('register/', usuarios_views.register_view, name='register'),
    
    # 🏠 Rutas de Gesicom (compañeros)
    path('home/', gesicom_views.home, name='home'),
    path('usuario/', gesicom_views.role_usuario, name='usuario'),
    path('nosotros/', gesicom_views.nosotros, name='nosotros'),
    path('contacto/', gesicom_views.contacto, name='contacto'),
    path('ayuda/', gesicom_views.ayuda, name='ayuda'),
    path('portal/', gesicom_views.portal, name='portal'),
    
    # 👥 RUTAS POR ROLES
    path('roles/instructor/', gesicom_views.role_instructor, name='role_instructor'),
    path('roles/instructor-table/', gesicom_views.instructor_table, name='instructor_table'),
    path('roles/investigador/', gesicom_views.role_investigador, name='role_investigador'),
    path('roles/dinamizador/', gesicom_views.role_dinamizador, name='role_dinamizador'),
    path('roles/coordinador/', gesicom_views.role_coordinador, name='role_coordinador'),
    path('access-denied/', gesicom_views.access_denied, name='access_denied'),
    
    # 🔑 Recuperación de contraseña (compañeros)
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Registro/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Registro/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Registro/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Registro/password_reset_complete.html'), name='password_reset_complete'),
    
    # 🔐 Recuperación con código (app cuentas)
    path('olvide-password/', cuentas_views.olvide_password, name='olvide_password'),
    path('verificar-codigo/', cuentas_views.verificar_codigo, name='verificar_codigo'),
    path('restablecer-password/', cuentas_views.restablecer_password, name='restablecer_password'),
]
