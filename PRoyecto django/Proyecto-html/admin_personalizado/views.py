<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.contrib import messages


def _require_administrador(user):
    """Verifica que el usuario tenga el rol de administrador o sea superuser."""
    return user.is_superuser or user.groups.filter(name='administrador').exists()


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def dashboard(request):
    """Dashboard principal del panel de administración."""
    total_users = User.objects.count()
    total_groups = Group.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    context = {
        'total_users': total_users,
        'total_groups': total_groups,
        'active_users': active_users,
>>>>>>> Falcaoperez
    }
    return render(request, 'admin_personalizado/dashboard.html', context)


@login_required
<<<<<<< HEAD
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
=======
@user_passes_test(_require_administrador, login_url='access_denied')
def usuarios(request):
    """Lista de usuarios con paginación y búsqueda."""
    users_list = User.objects.all().prefetch_related('groups').order_by('-date_joined')

    # Paginación
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    context = {
        'users': users,
    }
    return render(request, 'admin_personalizado/usuarios.html', context)


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def permisos(request):
    """Gestión de permisos de grupos."""
    groups = Group.objects.all().order_by('name')
    selected_group = None
    permissions = []

    # Si se envió el formulario
    if request.method == 'POST':
        group_id = request.POST.get('group')
        if group_id:
            try:
                selected_group = Group.objects.get(id=group_id)

                # Procesar cada permiso enviado
                for key, value in request.POST.items():
                    if key.startswith('perm_') and '_1' in key:
                        # Extraer el codename del permiso
                        codename = key.replace('perm_', '').replace('_1', '')
                        permission_value = value

                        # Buscar el permiso en la base de datos
                        try:
                            permission = Permission.objects.get(codename=codename)

                            # Si es "allowed", agregar el permiso al grupo
                            if permission_value == 'allowed':
                                selected_group.permissions.add(permission)
                            # Si es "denied" o "inherited", remover el permiso del grupo
                            else:
                                selected_group.permissions.remove(permission)
                        except Permission.DoesNotExist:
                            # El permiso no existe, ignorar
                            pass

                messages.success(request, f'Permisos del grupo {selected_group.name} actualizados correctamente.')
                return redirect(f"{request.path}?group={group_id}")
            except Group.DoesNotExist:
                messages.error(request, 'El grupo seleccionado no existe.')

    # Obtener el grupo seleccionado para mostrar
    group_id = request.GET.get('group')
    if group_id:
        try:
            selected_group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            messages.error(request, 'El grupo seleccionado no existe.')

    # Preparar los datos de permisos para mostrar
    if selected_group:
        # Obtener todos los permisos del grupo
        group_permissions = selected_group.permissions.all()
        permission_codenames = [p.codename for p in group_permissions]

        # Definir las acciones a mostrar
        permissions_data = [
            {
                'label': 'Configurar',
                'codename': 'change_envio',
                'status_1': 'allowed' if 'change_envio' in permission_codenames else 'inherited',
                'status_2': 'allowed',
            },
            {
                'label': 'Crear',
                'codename': 'add_envio',
                'status_1': 'allowed' if 'add_envio' in permission_codenames else 'inherited',
                'status_2': 'allowed',
            },
            {
                'label': 'Borrar',
                'codename': 'delete_envio',
                'status_1': 'allowed' if 'delete_envio' in permission_codenames else 'inherited',
                'status_2': 'inherited',
            },
            {
                'label': 'Editar',
                'codename': 'change_envio',
                'status_1': 'allowed' if 'change_envio' in permission_codenames else 'inherited',
                'status_2': 'allowed',
            },
            {
                'label': 'Editar estado',
                'codename': 'change_user',
                'status_1': 'allowed' if 'change_user' in permission_codenames else 'inherited',
                'status_2': 'allowed',
            },
            {
                'label': 'Acceso a la interfaz de administración',
                'codename': 'view_logentry',
                'status_1': 'allowed' if 'view_logentry' in permission_codenames else 'inherited',
                'status_2': 'inherited',
            },
            {
                'label': 'Solo opciones de configuración',
                'codename': 'view_envio',
                'status_1': 'allowed' if 'view_envio' in permission_codenames else 'inherited',
                'status_2': 'inherited',
            },
        ]

        permissions = permissions_data

    context = {
        'groups': groups,
        'selected_group': selected_group,
        'permissions': permissions,
    }
    return render(request, 'admin_personalizado/permisos.html', context)
>>>>>>> Falcaoperez
