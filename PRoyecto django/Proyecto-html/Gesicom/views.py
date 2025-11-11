from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    # Mantener compatibilidad; usar home como contenido principal
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')
def login_view(request):
    # Capturar rol desde GET o POST para personalizar y redirigir
    role = request.GET.get('role') or request.POST.get('role') or ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir según rol seleccionado
            role_routes = {
                'instructor': 'role_instructor',
                'investigador': 'role_investigador',
                'dinamizador': 'role_dinamizador',
                'coordinador': 'role_coordinador',
            }
            target = role_routes.get(role, 'home')
            return redirect(target)
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos',
                'role': role,
                'username': username,
            })
    # GET: mostrar formulario con el rol si viene en la URL
    return render(request, 'login.html', {'role': role})

def register_view(request):
    # Permite registrar un usuario y luego redirige al login, preservando el rol si viene en la URL
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
        # Tras crear el usuario, redirigir al login del rol (si existe)
        login_url = 'login'
        if role:
            return redirect(f"/{login_url}/?role={role}")
        return redirect(login_url)

    return render(request, 'register.html', {'role': role})

def role_instructor(request):
    return render(request, 'roles/instructor.html')

def role_investigador(request):
    return render(request, 'roles/investigador.html')

def role_dinamizador(request):
    return render(request, 'roles/dinamizador.html')

def role_coordinador(request):
    return render(request, 'roles/coordinador.html')

def portal(request):
    # Redirige al selector de roles (home)
    return redirect('home')
