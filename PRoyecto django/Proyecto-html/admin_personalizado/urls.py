from django.urls import path
from . import views

app_name = 'admin_personalizado'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('usuario/<int:user_id>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuario/<int:user_id>/grupo/', views.asignar_grupo, name='asignar_grupo'),
    path('usuario/<int:user_id>/estado/', views.activar_desactivar_usuario, name='activar_desactivar'),
]
