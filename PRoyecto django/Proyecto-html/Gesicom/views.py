from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Envio

def index(request):
    # Mantener compatibilidad; usar home como contenido principal
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    return render(request, 'contacto.html')

def ayuda(request):
    return render(request, 'ayuda.html')

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

        # Validación de contraseña del lado servidor (usa AUTH_PASSWORD_VALIDATORS)
        try:
            validate_password(password1)
        except ValidationError as e:
            errors.extend(list(e.messages))
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

def evidencia(request):
    # Formulario de envío de evidencias: guarda archivo y link
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        proyecto = (request.POST.get('opcion', '') or '').strip()
        tipos = request.POST.getlist('evidencias')
        tipo_evidencia = ', '.join(tipos) if tipos else 'Sin especificar'
        link = request.POST.get('linkArchivo', '').strip()
        archivo = request.FILES.get('archivo')
        observaciones = request.POST.get('observaciones', '').strip()

        errors = []
        if not (link or archivo):
            errors.append('Debe proporcionar un enlace o adjuntar un archivo (al menos uno).')
        if not nombre:
            errors.append('El nombre es obligatorio.')
        if not proyecto:
            errors.append('Debe seleccionar el proyecto.')

        if errors:
            return render(request, 'formulario.html', {
                'errors': errors,
                'success': False,
                'nombre': nombre,
                'proyecto': proyecto,
                'tipos': tipos,
                'linkArchivo': link,
                'observaciones': observaciones,
            })

        envio = Envio(
            nombre=nombre,
            proyecto=proyecto,
            tipo_evidencia=tipo_evidencia,
            link_evidencia=link,
            archivo_evidencia=archivo,
            observaciones=observaciones,
        )
        envio.save()
        return render(request, 'formulario.html', {'success': True})

    return render(request, 'formulario.html')

def evidencias_list(request):
    qs = Envio.objects.all()

    # Filtro por proyecto
    proyecto = request.GET.get('proyecto', '')
    if proyecto:
        qs = qs.filter(proyecto=proyecto)

    # Búsqueda por nombre, tipo y observaciones
    q = (request.GET.get('q') or '').strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(tipo_evidencia__icontains=q) |
            Q(observaciones__icontains=q)
        )

    # Ordenamiento
    order = request.GET.get('order', 'fecha_envio')
    direction = request.GET.get('dir', 'desc')
    allowed = {'fecha_envio', 'nombre', 'proyecto', 'tipo_evidencia'}
    if order in allowed:
        sort = order if direction == 'asc' else f'-{order}'
        qs = qs.order_by(sort)
    else:
        qs = qs.order_by('-fecha_envio')

    # Paginación (tamaño fijo)
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'envios': page_obj,
        'proyecto': proyecto,
        'order': order,
        'dir': direction,
        'q': q,
    }
    return render(request, 'evidencias_list.html', context)
