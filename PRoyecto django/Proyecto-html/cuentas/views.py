from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import random, datetime

# GUARDAR CÓDIGOS TEMPORALES
codigos = {}
User = get_user_model()

def olvide_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
@csrf_exempt
def olvide_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    email = request.POST.get("email")
    if not email:
        return JsonResponse({"error": "Correo requerido"}, status=400)

    if not User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Correo no registrado"}, status=400)

    codigo = random.randint(100000, 999999)
    expira = timezone.now() + datetime.timedelta(minutes=10)
    codigos[email] = {"codigo": codigo, "expira": expira}

    send_mail(
        "Código de recuperación",
        f"Tu código es: {codigo}. Expira en 10 minutos.",
        "no-reply@gmail.com",
        [email],
        fail_silently=True,
    )

    return JsonResponse({"mensaje": "Código enviado al correo."})
@csrf_exempt
def verificar_codigo(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    email = request.POST.get("email")
    codigo_raw = request.POST.get("codigo")
    if not email or not codigo_raw:
        return JsonResponse({"error": "Datos incompletos"}, status=400)
    try:
        codigo = int(codigo_raw)
    except ValueError:
        return JsonResponse({"error": "Código inválido"}, status=400)

    if email not in codigos:
        return JsonResponse({"error": "No se solicitó código"}, status=400)

    data = codigos[email]

    if timezone.now() > data["expira"]:
        return JsonResponse({"error": "Código expirado"}, status=400)

    if codigo != data["codigo"]:
        return JsonResponse({"error": "Código incorrecto"}, status=400)

    return JsonResponse({"mensaje": "Código correcto"})
@csrf_exempt
def restablecer_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    email = request.POST.get("email")
    codigo = request.POST.get("codigo")
    nueva = request.POST.get("password")

    if not email or not codigo or not nueva:
        return JsonResponse({"error": "Datos incompletos"}, status=400)

    if email not in codigos:
        return JsonResponse({"error": "No se solicitó código"}, status=400)

    data = codigos[email]
    try:
        codigo = int(codigo)
    except ValueError:
        return JsonResponse({"error": "Código inválido"}, status=400)

    if timezone.now() > data["expira"]:
        return JsonResponse({"error": "Código expirado"}, status=400)

    if codigo != data["codigo"]:
        return JsonResponse({"error": "Código incorrecto"}, status=400)

    user = User.objects.filter(email=email).first()
    if not user:
        return JsonResponse({"error": "Correo no registrado"}, status=400)

    user.set_password(nueva)
    user.save()

    # eliminar código usado
    if email in codigos:
        del codigos[email]

    return JsonResponse({"mensaje": "Contraseña cambiada con éxito"})
