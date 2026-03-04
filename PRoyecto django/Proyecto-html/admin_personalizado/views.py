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


