from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from .models import Envio
from django.http import HttpResponse
import csv
import datetime
import calendar

def _in_group(name):
    def check(u):
        if u.is_superuser or u.groups.filter(name='administrador').exists():
            return True
        return u.groups.filter(name=name).exists()
    return check

def index(request):
    # Mantener compatibilidad; usar home como contenido principal
    return render(request, 'home.html')

def home(request):
    is_basic = False
    if request.user.is_authenticated:
        is_basic = request.user.groups.filter(name='usuario').exists()
    return render(request, 'home.html', {'is_basic_user': is_basic})

@login_required
@user_passes_test(_in_group('usuario'), login_url='access_denied')
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


@login_required
@user_passes_test(_in_group('instructor'), login_url='access_denied')
def role_instructor(request):
    return render(request, 'roles/instructor.html')

@login_required
@user_passes_test(_in_group('investigador'), login_url='access_denied')
def role_investigador(request):
    return render(request, 'roles/investigador.html')

@login_required
@user_passes_test(_in_group('dinamizador'), login_url='access_denied')
def role_dinamizador(request):
    return render(request, 'roles/dinamizador.html')

@login_required
@user_passes_test(_in_group('coordinador'), login_url='access_denied')
def role_coordinador(request):
    return render(request, 'roles/coordinador.html')

def portal(request):
    # Redirige al selector de roles (home)
    return redirect('home')

def admin_menu(request):
    return render(request, 'admin/menu.html')

def proyecciones(request):
    categoria_stats = (
        Envio.objects.values('tipo_evidencia')
        .annotate(total=Count('id'))
        .order_by('-total', 'tipo_evidencia')
    )
    proyecto_stats = (
        Envio.objects.values('proyecto')
        .annotate(total=Count('id'))
        .order_by('-total', 'proyecto')
    )
    total_envios = Envio.objects.count()

    categoria_stats = [
        {
            'tipo_evidencia': item['tipo_evidencia'] or 'Sin categoría',
            'total': item['total'],
            'porcentaje': round((item['total'] / total_envios) * 100, 2) if total_envios else 0,
        }
        for item in categoria_stats
    ]
    proyecto_stats = [
        {
            'proyecto': item['proyecto'] or 'Sin proyecto',
            'total': item['total'],
            'porcentaje': round((item['total'] / total_envios) * 100, 2) if total_envios else 0,
        }
        for item in proyecto_stats
    ]

    context = {
        'total_envios': total_envios,
        'categoria_stats': categoria_stats,
        'proyecto_stats': proyecto_stats,
    }
    return render(request, 'admin/proyecciones.html', context)

def reportes(request):
    proyecto = request.GET.get('proyecto', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    qs = Envio.objects.all()
    if proyecto:
        qs = qs.filter(proyecto=proyecto)

    def parse_month(s):
        try:
            year, month = map(int, s.split('-'))
            return datetime.date(year, month, 1)
        except Exception:
            return None

    start_date = parse_month(start) if start else None
    end_date = parse_month(end) if end else None
    if end_date:
        last_day = calendar.monthrange(end_date.year, end_date.month)[1]
        end_date = datetime.date(end_date.year, end_date.month, last_day)
    if start_date:
        qs = qs.filter(fecha_envio__gte=start_date)
    if end_date:
        qs = qs.filter(fecha_envio__lte=end_date)

    total_envios = qs.count()
    categoria_stats_qs = (
        qs.values('tipo_evidencia')
        .annotate(total=Count('id'))
        .order_by('-total', 'tipo_evidencia')
    )
    categoria_stats = [
        {
            'tipo_evidencia': item['tipo_evidencia'] or 'Sin categoría',
            'total': item['total'],
            'porcentaje': round((item['total'] / total_envios) * 100, 2) if total_envios else 0,
        }
        for item in categoria_stats_qs
    ]

    monthly_qs = (
        qs.annotate(month=TruncMonth('fecha_envio'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    monthly_stats = [
        {
            'month': item['month'],
            'total': item['total'],
            'porcentaje': round((item['total'] / total_envios) * 100, 2) if total_envios else 0,
        }
        for item in monthly_qs
    ]

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
    proyecto = request.GET.get('proyecto', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    qs = Envio.objects.all()
    if proyecto:
        qs = qs.filter(proyecto=proyecto)

    def parse_month(s):
        try:
            year, month = map(int, s.split('-'))
            return datetime.date(year, month, 1)
        except Exception:
            return None

    start_date = parse_month(start) if start else None
    end_date = parse_month(end) if end else None
    if end_date:
        last_day = calendar.monthrange(end_date.year, end_date.month)[1]
        end_date = datetime.date(end_date.year, end_date.month, last_day)
    if start_date:
        qs = qs.filter(fecha_envio__gte=start_date)
    if end_date:
        qs = qs.filter(fecha_envio__lte=end_date)

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

@login_required
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

def access_denied(request):
    return render(request, 'access_denied.html')

@login_required
@user_passes_test(lambda u: (u.is_superuser or u.groups.filter(name='administrador').exists() or u.groups.filter(name__in=['coordinador','dinamizador']).exists()), login_url='access_denied')
def instructor_table(request):
    qs = Envio.objects.all().order_by('-fecha_envio')
    return render(request, 'roles/instructor_table.html', {'envios': qs})
