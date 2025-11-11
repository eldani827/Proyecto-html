"""
URL configuration for SENNOVA project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Gesicom import views as gesicom_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inicio del sitio apunta a home
    path('', gesicom_views.home, name='home'),
    path('login/', gesicom_views.login_view, name='login'),
    path('register/', gesicom_views.register_view, name='register'),
    path('portal/', gesicom_views.portal, name='portal'),
    path('roles/instructor/', gesicom_views.role_instructor, name='role_instructor'),
    path('roles/investigador/', gesicom_views.role_investigador, name='role_investigador'),
    path('roles/dinamizador/', gesicom_views.role_dinamizador, name='role_dinamizador'),
    path('roles/coordinador/', gesicom_views.role_coordinador, name='role_coordinador'),
    # Evidencias: formulario de envío
    path('evidencia/', gesicom_views.evidencia, name='evidencia'),
    path('evidencias/', gesicom_views.evidencias_list, name='evidencias_list'),
    # Password reset flow
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)