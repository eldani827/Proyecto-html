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
