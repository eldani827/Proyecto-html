from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


def es_admin_personalizado(user):
    """Verifica si el usuario tiene permiso para acceder al admin personalizado."""
    return user and user.groups.filter(name='administrador').exists()


@login_required
def admin_dashboard(request):
    """Dashboard del admin personalizado."""
    if not es_admin_personalizado(request.user):
        return redirect('access_denied')
    
    # Estadísticas
    total_usuarios = User.objects.count()
    grupos_disponibles = Group.objects.all()
    usuarios_por_grupo = {}
    for grupo in grupos_disponibles:
        usuarios_por_grupo[grupo.name] = grupo.user_set.count()
    
    context = {
        'total_usuarios': total_usuarios,
        'grupos_disponibles': grupos_disponibles,
        'usuarios_por_grupo': usuarios_por_grupo,
    }
    return render(request, 'admin_personalizado/dashboard.html', context)


@login_required
def gestionar_usuarios(request):
    """Listar y buscar usuarios."""
    if not es_admin_personalizado(request.user):
        return redirect('access_denied')
    
    busqueda = request.GET.get('q', '').strip()
    usuarios = User.objects.all()
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        )
    
    usuarios = usuarios.order_by('username')
    grupos = Group.objects.all()
    
    context = {
        'usuarios': usuarios,
        'grupos': grupos,
        'busqueda': busqueda,
    }
    return render(request, 'admin_personalizado/gestionar_usuarios.html', context)


@login_required
@require_http_methods(["GET"])
def detalle_usuario(request, user_id):
    """Detalles de un usuario y asignación de grupos."""
    if not es_admin_personalizado(request.user):
        return redirect('access_denied')
    
    usuario = get_object_or_404(User, pk=user_id)
    grupos_disponibles = Group.objects.all()
    grupos_usuario = usuario.groups.all()
    
    context = {
        'usuario': usuario,
        'grupos_disponibles': grupos_disponibles,
        'grupos_usuario': grupos_usuario,
    }
    return render(request, 'admin_personalizado/detalle_usuario.html', context)


@login_required
@require_http_methods(["POST"])
def asignar_grupo(request, user_id):
    """Asignar o quitar grupo a un usuario (AJAX)."""
    if not es_admin_personalizado(request.user):
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    usuario = get_object_or_404(User, pk=user_id)
    grupo_id = request.POST.get('grupo_id')
    accion = request.POST.get('accion')  # 'agregar' o 'quitar'
    
    if not grupo_id or accion not in ['agregar', 'quitar']:
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
    
    grupo = get_object_or_404(Group, pk=grupo_id)
    
    try:
        if accion == 'agregar':
            usuario.groups.add(grupo)
            logger.info(f"{request.user.username} asignó grupo '{grupo.name}' a {usuario.username}")
            mensaje = f"Grupo '{grupo.name}' asignado a {usuario.username}"
        else:
            usuario.groups.remove(grupo)
            logger.info(f"{request.user.username} removió grupo '{grupo.name}' de {usuario.username}")
            mensaje = f"Grupo '{grupo.name}' removido de {usuario.username}"
        
        return JsonResponse({'mensaje': mensaje, 'success': True})
    except Exception as e:
        logger.error(f"Error al asignar grupo: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def activar_desactivar_usuario(request, user_id):
    """Activar/desactivar usuario (AJAX)."""
    if not es_admin_personalizado(request.user):
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    usuario = get_object_or_404(User, pk=user_id)
    accion = request.POST.get('accion')  # 'activar' o 'desactivar'
    
    if accion not in ['activar', 'desactivar']:
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
    
    try:
        usuario.is_active = accion == 'activar'
        usuario.save()
        logger.info(f"{request.user.username} {accion} usuario {usuario.username}")
        estado = "activado" if usuario.is_active else "desactivado"
        return JsonResponse({'mensaje': f"Usuario {estado}", 'success': True})
    except Exception as e:
        logger.error(f"Error al cambiar estado: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
