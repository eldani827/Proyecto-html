from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html')


def login_view(request):
    role_param = request.GET.get('role') or request.POST.get('role')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir según rol
            role_to_route = {
                'instructor': 'role_instructor',
                'investigador': 'role_investigador',
                'dinamizador': 'role_dinamizador',
                'coordinador': 'role_coordinador',
            }
            if role_param in role_to_route:
                return redirect(role_to_route[role_param])
            return redirect('index')
        else:
            context = {
                'error': 'Usuario o contraseña incorrectos.',
                'username': username,
                'role': role_param,
            }
            return render(request, 'login.html', context)

    return render(request, 'login.html', { 'role': role_param })


def portal(request):
    return render(request, 'portal.html')


def role_instructor(request):
    return render(request, 'roles/instructor.html')


def role_investigador(request):
    return render(request, 'roles/investigador.html')


def role_dinamizador(request):
    return render(request, 'roles/dinamizador.html')


def role_coordinador(request):
    return render(request, 'roles/coordinador.html')
