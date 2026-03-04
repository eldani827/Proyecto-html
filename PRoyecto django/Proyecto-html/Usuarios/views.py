from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth.models import User, Group
import logging
import traceback
from django.db import transaction, IntegrityError

logger = logging.getLogger(__name__)


ROLE_ROUTES = {
    'instructor': 'role_instructor',
    'investigador': 'role_investigador',
    'dinamizador': 'role_dinamizador',
    'coordinador': 'role_coordinador',
    'usuario': 'usuario',
}


def _validate_password(password1, password2=None):
    errors = []

    if not password1:
        errors.append('La contraseña es obligatoria.')
        return errors

    if password2 and password1 != password2:
        errors.append('Las contraseñas no coinciden.')
        return errors

    if len(password1) != 8:
        errors.append('La contraseña debe tener exactamente 8 caracteres.')

    has_upper = re.search(r'[A-Z]', password1) is not None
    has_digit = re.search(r'\d', password1) is not None
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password1) is not None

    if not has_upper:
        errors.append('Debe contener al menos una letra mayúscula.')

    if not (has_digit or has_special):
        errors.append('Debe contener al menos un número o carácter especial.')

    return errors


def login_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if role not in ROLE_ROUTES:
        role = ''

    if request.method == 'POST':
        username_input = (request.POST.get('username', '') or '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')

        # Si el usuario escribió un correo, intentar resolver su username
        username_for_auth = username_input
        if '@' in username_input and not User.objects.filter(username=username_input).exists():
            try:
                u = User.objects.get(email__iexact=username_input)
                username_for_auth = u.username
            except User.DoesNotExist:
                # no existe un usuario con ese email
                pass

        user = authenticate(request, username=username_for_auth, password=password)
        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(60 * 60 * 24 * 14)
            else:
                request.session.set_expiry(0)
            if user.is_superuser:
                return redirect('admin:index')

            user_groups = set(user.groups.values_list('name', flat=True))

            if 'administrador' in user_groups:
                return redirect('admin_menu')

            if role and role in ROLE_ROUTES:
                return redirect(ROLE_ROUTES[role])

            target = 'usuario' if 'usuario' in user_groups else 'home'
            return redirect(target)

        return render(request, 'login.html', {
            'error': 'Usuario o contraseña incorrectos',
            'role': role,
            'username': username_input,
        })

    return render(request, 'login.html', {'role': role})


def register_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        username = (request.POST.get('username', '') or '').strip()
        email = (request.POST.get('email', '') or '').strip().lower()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not username:
            errors.append('El usuario es obligatorio.')
        if not email:
            errors.append('El correo es obligatorio.')

        errors.extend(_validate_password(password1, password2))

        if User.objects.filter(username=username).exists():
            errors.append('Ese usuario ya existe. Prueba con otro.')

        if User.objects.filter(email=email).exists():
            errors.append('Ese correo ya está registrado.')

        if errors:
            return render(request, 'register.html', {
                'errors': errors,
                'role': role,
                'username': username,
                'email': email,
            })

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password1)
                g, _ = Group.objects.get_or_create(name='usuario')
                user.groups.add(g)
                user.save()
            login(request, user)
            target = ROLE_ROUTES.get(role, 'usuario')
            return redirect(target)
        except IntegrityError:
            errors.append('El usuario o correo ya existe.')
            return render(request, 'register.html', {
                'errors': errors,
                'role': role,
                'username': username,
                'email': email,
            })
        except Exception:
            tb = traceback.format_exc()
            logger.exception('Error creando usuario')
            errors.append('Error interno al crear la cuenta. Contacta al administrador.')
            return render(request, 'register.html', {
                'errors': errors,
                'role': role,
                'username': username,
                'email': email,
                'debug_trace': tb,
            })

    return render(request, 'register.html', {'role': role})


@login_required(login_url='login')
def panel_usuario(request):
    """Vista del panel personal del usuario."""
    return render(request, 'usuario/panel_usuario.html')


def logout_view(request):
    """Cerrar sesión del usuario."""
    logout(request)
    return redirect('login')

