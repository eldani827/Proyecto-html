from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')

def role_instructor(request):
    return render(request, 'role_instructor.html')

def role_investigador(request):
    return render(request, 'role_investigador.html')

def role_dinamizador(request):
    return render(request, 'role_dinamizador.html')

def role_coordinador(request):
    return render(request, 'role_coordinador.html')
