from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
import random, datetime

# SIMULAR USUARIOS
usuarios = {
    "usuario@example.com": {"password": "1234"}
}

# GUARDAR CÓDIGOS TEMPORALES
codigos = {}

def olvide_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    email = request.POST.get("email")

    if email not in usuarios:
        return JsonResponse({"error": "Correo no registrado"}, status=400)

    # generar código
    codigo = random.randint(100000, 999999)
    expira = timezone.now() + datetime.timedelta(minutes=10)

    codigos[email] = {"codigo": codigo, "expira": expira}

    # enviar correo
    send_mail(
        "Código de recuperación",
        f"Tu código es: {codigo}. Expira en 10 minutos.",
        "tu_correo@gmail.com",
        [email],
    )

    return JsonResponse({"mensaje": "Código enviado al correo."})

def verificar_codigo(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    email = request.POST.get("email")
    codigo = int(request.POST.get("codigo"))

    if email not in codigos:
        return JsonResponse({"error": "No se solicitó código"}, status=400)

    data = codigos[email]

    if timezone.now() > data["expira"]:
        return JsonResponse({"error": "Código expirado"}, status=400)

    if codigo != data["codigo"]:
        return JsonResponse({"error": "Código incorrecto"}, status=400)

    return JsonResponse({"mensaje": "Código correcto"})

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

    usuarios[email] = usuarios.get(email, {})
    usuarios[email]["password"] = nueva

    return JsonResponse({"mensaje": "Contraseña cambiada con éxito"})
