from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
import random
import datetime

User = get_user_model()


@require_http_methods(["POST"])
def olvide_password(request):
    email = request.POST.get("email", "").strip()
    if not email:
        return JsonResponse({"error": "Correo requerido"}, status=400)

    user = User.objects.filter(email=email).first()
    if not user:
        return JsonResponse({"error": "Si el correo existe, recibirás un mensaje"}, status=200)

    token = default_token_generator.make_token(user)
    
    try:
        send_mail(
            "Restablecer contraseña",
            f"Usa este link para restablecer tu contraseña (válido por 1 hora):\n"
            f"http://localhost:8000/reset/{user.pk}-{token}/",
            "no-reply@gesicom.com",
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({"error": f"Error al enviar correo: {str(e)}"}, status=500)

    return JsonResponse({"mensaje": "Enlace de restablecimiento enviado al correo"}, status=200)


@require_http_methods(["GET"])
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

