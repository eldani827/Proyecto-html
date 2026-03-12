from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv

# Permisos que se pueden gestionar desde la vista de permisos
USER_PERMISSIONS_SCOPE = [
    ('add_user', 'Crear usuario'),
    ('change_user', 'Editar usuario'),
    ('delete_user', 'Borrar usuario'),
    ('view_user', 'Ver usuario'),
]


def dashboard(request):
    total_users = User.objects.count()
    total_groups = Group.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    return render(request, 'admin_personalizado/dashboard.html', {
        'total_users': total_users,
        'total_groups': total_groups,
        'active_users': active_users,
    })


def usuarios(request):
    qs = User.objects.all().order_by('username')
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_personalizado/usuarios.html', {
        'users': page_obj,
    })


def permisos(request):
    grupos = Group.objects.all().order_by('name')
    
    # Obtener el grupo seleccionado
    group_name = request.GET.get('group') or request.POST.get('group')
    if not group_name and grupos.exists():
        group_name = grupos[0].name
        
    selected = Group.objects.filter(name=group_name).first() if group_name else None
    
    current_perms = set()
    if selected:
        current_perms = set(selected.permissions.values_list('codename', flat=True))
        
    if request.method == 'POST' and selected:
        desired_perms = set()
        for code, _ in USER_PERMISSIONS_SCOPE:
            if request.POST.get(f'perm_{code}') == 'on':
                desired_perms.add(code)
                
        # Obtener los objetos Permission correspondientes
        perms_to_manage = Permission.objects.filter(codename__in=[c for c, _ in USER_PERMISSIONS_SCOPE])
        perms_map = {p.codename: p for p in perms_to_manage}
        
        for code, _ in USER_PERMISSIONS_SCOPE:
            perm_obj = perms_map.get(code)
            if not perm_obj:
                continue
                
            if code in desired_perms and code not in current_perms:
                selected.permissions.add(perm_obj)
            elif code not in desired_perms and code in current_perms:
                selected.permissions.remove(perm_obj)
                
        # Actualizar permisos actuales después del POST
        current_perms = set(selected.permissions.values_list('codename', flat=True))
        
    return render(request, 'admin_personalizado/permisos.html', {
        'grupos': grupos,
        'group_name': group_name,
        'scope': USER_PERMISSIONS_SCOPE,
        'current': current_perms,
    })


def usuarios_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Email', 'Activo', 'Grupos'])
    
    for user in User.objects.all().order_by('username'):
        groups = ', '.join(user.groups.values_list('name', flat=True))
        is_active_str = 'Sí' if user.is_active else 'No'
        writer.writerow([user.username, user.email, is_active_str, groups])
        
    return response
