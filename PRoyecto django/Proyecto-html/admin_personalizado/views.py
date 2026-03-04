from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction, models
from django.db.models import Q
import re


def _require_administrador(user):
	"""Verifica que el usuario tenga el rol de administrador o sea superuser."""
	return user.is_superuser or user.groups.filter(name='administrador').exists()


def _validate_password(password):
	"""Valida que la contraseña cumpla con los requisitos."""
	errors = []
	
	if not password:
		errors.append('La contraseña es obligatoria.')
		return errors
	
	if len(password) != 8:
		errors.append('La contraseña debe tener exactamente 8 caracteres.')
	
	has_upper = re.search(r'[A-Z]', password) is not None
	has_digit = re.search(r'\d', password) is not None
	has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None
	
	if not has_upper:
		errors.append('Debe contener al menos una letra mayúscula.')
	
	if not (has_digit or has_special):
		errors.append('Debe contener al menos un número o carácter especial.')
	
	return errors


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
	}
	return render(request, 'admin_personalizado/dashboard.html', context)


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


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def gestionar_usuarios(request):
	"""Gestiona la lista de usuarios del sistema."""
	busqueda = request.GET.get('q', '').strip()
	
	usuarios_list = User.objects.all().prefetch_related('groups').order_by('-date_joined')
	
	# Filtrar por búsqueda
	if busqueda:
		usuarios_list = usuarios_list.filter(
			Q(username__icontains=busqueda) |
			Q(email__icontains=busqueda) |
			Q(first_name__icontains=busqueda) |
			Q(last_name__icontains=busqueda)
		)
	
	context = {
		'usuarios': usuarios_list,
		'busqueda': busqueda,
	}
	return render(request, 'admin_personalizado/gestionar_usuarios.html', context)


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def crear_usuario(request):
	"""Crea un nuevo usuario desde el panel de administración."""
	grupos_disponibles = Group.objects.all()
	
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip().lower()
		password = request.POST.get('password', '')
		password_confirm = request.POST.get('password_confirm', '')
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		grupos_ids = request.POST.getlist('grupos')
		
		errores = []
		
		# Validaciones
		if not username:
			errores.append('El nombre de usuario es obligatorio.')
		elif User.objects.filter(username=username).exists():
			errores.append('Ese nombre de usuario ya existe.')
		
		if not email:
			errores.append('El correo es obligatorio.')
		elif User.objects.filter(email=email).exists():
			errores.append('Ese correo ya está registrado.')
		
		errores.extend(_validate_password(password))
		
		if password != password_confirm:
			errores.append('Las contraseñas no coinciden.')
		
		if errores:
			context = {
				'grupos_disponibles': grupos_disponibles,
				'errores': errores,
				'username': username,
				'email': email,
				'first_name': first_name,
				'last_name': last_name,
			}
			return render(request, 'admin_personalizado/crear_usuario.html', context)
		
		try:
			with transaction.atomic():
				user = User.objects.create_user(
					username=username,
					email=email,
					password=password,
					first_name=first_name,
					last_name=last_name,
					is_active=True  # 👈 IMPORTANTE: Asegurar que el usuario sea activo
				)
				
				# Asignar grupos si se seleccionaron
				if grupos_ids:
					grupos = Group.objects.filter(id__in=grupos_ids)
					user.groups.set(grupos)
				
				messages.success(request, f'Usuario "{username}" creado correctamente y está ACTIVO.')
				return redirect('admin_personalizado:detalle_usuario', usuario_id=user.id)
		
		except Exception as e:
			messages.error(request, f'Error al crear el usuario: {str(e)}')
	
	context = {
		'grupos_disponibles': grupos_disponibles,
	}
	return render(request, 'admin_personalizado/crear_usuario.html', context)


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def detalle_usuario(request, usuario_id):
	"""Detalle y edición de un usuario."""
	usuario = get_object_or_404(User, id=usuario_id)
	grupos_disponibles = Group.objects.all()
	grupos_usuario = usuario.groups.all()
	
	if request.method == 'POST':
		action = request.POST.get('action')
		
		if action == 'update_profile':
			usuario.first_name = request.POST.get('first_name', '').strip()
			usuario.last_name = request.POST.get('last_name', '').strip()
			usuario.email = request.POST.get('email', '').strip()
			usuario.save()
			messages.success(request, f'Perfil de {usuario.username} actualizado correctamente.')
			
		elif action == 'update_status':
			is_active = request.POST.get('is_active') == 'on'
			usuario.is_active = is_active
			usuario.save()
			status = "activado" if is_active else "desactivado"
			messages.success(request, f'Usuario {usuario.username} {status} correctamente.')
			
		elif action == 'update_groups':
			grupos_ids = request.POST.getlist('grupos')
			usuario.groups.set(grupos_ids)
			messages.success(request, f'Grupos del usuario {usuario.username} actualizados.')
			
		elif action == 'change_password':
			nueva_password = request.POST.get('nueva_password', '')
			confirmar_password = request.POST.get('confirmar_password', '')
			
			errores = _validate_password(nueva_password)
			
			if nueva_password != confirmar_password:
				errores.append('Las contraseñas no coinciden.')
			
			if errores:
				for error in errores:
					messages.error(request, error)
			else:
				usuario.set_password(nueva_password)
				usuario.save()
				messages.success(request, f'Contraseña de {usuario.username} cambiada correctamente.')
		
		return redirect('admin_personalizado:detalle_usuario', usuario_id=usuario_id)
	
	context = {
		'usuario': usuario,
		'grupos_disponibles': grupos_disponibles,
		'grupos_usuario': grupos_usuario,
	}
	return render(request, 'admin_personalizado/detalle_usuario.html', context)


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def asignar_grupo(request, usuario_id):
	"""AJAX endpoint para asignar/remover grupos de usuarios."""
	usuario = get_object_or_404(User, id=usuario_id)
	
	if request.method == 'POST':
		accion = request.POST.get('accion')
		grupo_id = request.POST.get('grupo_id')
		
		try:
			grupo = Group.objects.get(id=grupo_id)
			
			if accion == 'agregar':
				usuario.groups.add(grupo)
				mensaje = f'Rol "{grupo.name}" agregado al usuario {usuario.username}'
			elif accion == 'quitar':
				usuario.groups.remove(grupo)
				mensaje = f'Rol "{grupo.name}" removido del usuario {usuario.username}'
			else:
				return redirect('admin_personalizado:detalle_usuario', usuario_id=usuario_id)
			
			messages.success(request, mensaje)
		except Group.DoesNotExist:
			messages.error(request, 'El grupo seleccionado no existe.')
	
	return redirect('admin_personalizado:detalle_usuario', usuario_id=usuario_id)


@login_required
@user_passes_test(_require_administrador, login_url='access_denied')
def activar_desactivar(request, usuario_id):
	"""AJAX endpoint para activar/desactivar usuarios."""
	usuario = get_object_or_404(User, id=usuario_id)
	
	if request.method == 'POST':
		accion = request.POST.get('accion')
		
		if accion == 'activar':
			usuario.is_active = True
			usuario.save()
			messages.success(request, f'Usuario {usuario.username} activado correctamente.')
		elif accion == 'desactivar':
			usuario.is_active = False
			usuario.save()
			messages.success(request, f'Usuario {usuario.username} desactivado correctamente.')
	
	return redirect('admin_personalizado:detalle_usuario', usuario_id=usuario_id)


