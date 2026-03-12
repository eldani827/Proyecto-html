from django.urls import path
from . import views

app_name = 'admin_personalizado'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('permisos/', views.permisos, name='permisos'),
    path('usuarios/csv/', views.usuarios_csv, name='usuarios_csv'),
]
