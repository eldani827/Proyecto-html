from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User, Group


def login_view(request):
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Try to find user by email if '@' is in the input
        username = username_or_email
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                pass
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
                # Determine target based on user's highest priority role
                if user.is_superuser or user.groups.filter(name='administrador').exists():
                    target = 'admin_menu'
                elif user.groups.filter(name='coordinador').exists():
                    target = 'role_coordinador'
                elif user.groups.filter(name='instructor').exists():
                    target = 'role_instructor'
                elif user.groups.filter(name='investigador').exists():
                    target = 'role_investigador'
                elif user.groups.filter(name='dinamizador').exists():
                    target = 'role_dinamizador'
                elif user.groups.filter(name='usuario').exists():
                    target = 'usuario'
                else:
                    target = 'home'
            return redirect(target)
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos',
                'role': role,
                'username': username_or_email,
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

        # Use Django's password validators
        try:
            validate_password(password1)
        except ValidationError as e:
            errors.extend(e.messages)
        
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
