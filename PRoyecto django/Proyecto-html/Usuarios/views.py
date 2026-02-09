from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import re
from django.contrib.auth.models import User, Group


def login_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            if user.groups.filter(name='administrador').exists():
                return redirect('admin_menu')
            role_routes = {
                'instructor': 'role_instructor',
                'investigador': 'role_investigador',
                'dinamizador': 'role_dinamizador',
                'coordinador': 'role_coordinador',
                'usuario': 'usuario',
            }
            if role:
                target = role_routes.get(role, 'home')
            else:
                target = (
                    'usuario'
                    if user.groups.filter(name='usuario').exists()
                    else 'home'
                )
            return redirect(target)
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos',
                'role': role,
                'username': username,
            })
    return render(request, 'login.html', {'role': role})


def register_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not username:
            errors.append('El usuario es obligatorio.')
        if not email:
            errors.append('El correo es obligatorio.')
        if password1 != password2:
            errors.append('Las contraseñas no coinciden.')

        # Validar: 8 caracteres exactamente, 1+ mayúscula, 1+ dígito O carácter especial
        # Pattern: ^(?=.*[A-Z])(?=.*[\d\W])[A-Za-z\d\W]{8}$
        has_upper = re.search(r'[A-Z]', password1) is not None
        has_digit_or_special = re.search(r'[\d\W]', password1) is not None
        if not (len(password1) == 8 and has_upper and has_digit_or_special):
            errors.append(
                'La contraseña debe tener exactamente 8 caracteres, '
                'al menos una letra mayúscula y un número o carácter especial.'
            )
        if User.objects.filter(username=username).exists():
            errors.append('Ese usuario ya existe. Prueba con otro.')

        if errors:
            return render(request, 'register.html', {
                'errors': errors,
                'role': role,
                'username': username,
                'email': email,
            })

        user = User.objects.create_user(username=username, email=email, password=password1)
        g, _ = Group.objects.get_or_create(name='usuario')
        user.groups.add(g)
        login(request, user)
        role_routes = {
            'instructor': 'role_instructor',
            'investigador': 'role_investigador',
            'dinamizador': 'role_dinamizador',
            'coordinador': 'role_coordinador',
            'usuario': 'usuario',
        }
        target = role_routes.get(role, 'usuario')
        return redirect(target)

    return render(request, 'register.html', {'role': role})
