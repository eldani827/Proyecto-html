"""Vistas de la app 'Gesicom'.

Incluye:
- Páginas públicas (home, contacto, ayuda)
- Gestión y listas de envíos de evidencia
- Reportes y exportación CSV
- Control de acceso por grupos/roles
"""
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Envio
from .utils import (
    require_group, is_admin_or_group, apply_date_filters,
    calculate_stats, calculate_monthly_stats
)
from django.http import HttpResponse
import csv


def index(request):
    # Mantener compatibilidad; usar home como contenido principal
    return render(request, 'home.html')


def home(request):
    is_basic = False
    if request.user.is_authenticated:
        is_basic = request.user.groups.filter(name='usuario').exists()
    return render(request, 'home.html', {'is_basic_user': is_basic})


@require_group('usuario')
def role_usuario(request):
    return render(request, 'home.html', {'is_basic_user': True})


def nosotros(request):
    return render(request, 'nosotros.html')


def contacto(request):
    return render(request, 'contacto.html')


def ayuda(request):
    return render(request, 'ayuda.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@require_group('instructor')
def role_instructor(request):
    return render(request, 'roles/instructor.html')


@require_group('investigador')
def role_investigador(request):
    return render(request, 'roles/investigador.html')


@require_group('dinamizador')
def role_dinamizador(request):
    return render(request, 'roles/dinamizador.html')


@require_group('coordinador')
def role_coordinador(request):
    return render(request, 'roles/coordinador.html')


def portal(request):
    # Redirige al selector de roles (home)
    return redirect('home')


def admin_menu(request):
    return render(request, 'admin/menu.html')

def proyecciones(request):
    """Muestra estadísticas generales de envíos."""
    qs = Envio.objects.all()
    
    # Calcular estadísticas por tipo de evidencia
    categoria_stats, total_envios = calculate_stats(qs, 'tipo_evidencia')
    
    # Calcular estadísticas por proyecto
    proyecto_stats, _ = calculate_stats(qs, 'proyecto')
    
    # Reemplazar claves para coherencia con template
    categoria_stats = [
        {'tipo_evidencia': s['field_value'], 'total': s['total'], 'porcentaje': s['porcentaje']}
        for s in categoria_stats
    ]
    proyecto_stats = [
        {'proyecto': s['field_value'], 'total': s['total'], 'porcentaje': s['porcentaje']}
        for s in proyecto_stats
    ]

    context = {
        'total_envios': total_envios,
        'categoria_stats': categoria_stats,
        'proyecto_stats': proyecto_stats,
    }
    return render(request, 'admin/proyecciones.html', context)


def reportes(request):
    """Genera reportes filtrados de envíos."""
    proyecto = request.GET.get('proyecto', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    qs = Envio.objects.all()
    if proyecto:
        qs = qs.filter(proyecto=proyecto)
    
    qs = apply_date_filters(qs, start, end)

    # Calcular estadísticas por categoría
    categoria_stats, total_envios = calculate_stats(qs, 'tipo_evidencia')
    categoria_stats = [
        {'tipo_evidencia': s['field_value'], 'total': s['total'], 'porcentaje': s['porcentaje']}
        for s in categoria_stats
    ]
    
    # Calcular estadísticas mensuales
    monthly_stats, _ = calculate_monthly_stats(qs)

    proyecto_choices = [p for p, _ in Envio.PROYECTO_CHOICES]

    context = {
        'proyecto': proyecto,
        'start': start,
        'end': end,
        'proyecto_choices': proyecto_choices,
        'monthly_stats': monthly_stats,
        'categoria_stats': categoria_stats,
    }
    return render(request, 'admin/reportes.html', context)


def reportes_csv(request):
    """Exporta reportes filtrados en formato CSV."""
    proyecto = request.GET.get('proyecto', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    qs = Envio.objects.all()
    if proyecto:
        qs = qs.filter(proyecto=proyecto)
    
    qs = apply_date_filters(qs, start, end)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reportes.csv"'
    writer = csv.writer(response)
    writer.writerow(['fecha_envio', 'nombre', 'proyecto', 'tipo_evidencia', 'link_evidencia', 'observaciones'])
    for e in qs.order_by('fecha_envio'):
        writer.writerow([
            e.fecha_envio.isoformat() if e.fecha_envio else '',
            e.nombre,
            e.proyecto,
            e.tipo_evidencia,
            e.link_evidencia or '',
            (e.observaciones or '').replace('\r\n', ' ').replace('\n', ' '),
        ])
    return response


@login_required
def evidencia(request):
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
            usuario=request.user,
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


@login_required
def evidencias_list(request):
    """Lista de envíos con filtros, búsqueda y paginación."""
    qs = Envio.objects.select_related('usuario').all()

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


def access_denied(request):
    return render(request, 'access_denied.html')


@require_group('coordinador', 'dinamizador')
def instructor_table(request):
    """Muestra tabla de envíos para coordinadores y dinamizadores."""
    qs = Envio.objects.select_related('usuario').order_by('-fecha_envio')
    return render(request, 'roles/instructor_table.html', {'envios': qs})
