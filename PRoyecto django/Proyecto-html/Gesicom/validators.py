import re
from django.core.exceptions import ValidationError


class EightCharUpperNumberOrSpecialValidator:
    """
    Enforce password rules:
    - Exactly 8 characters
    - At least one uppercase letter
    - At least one digit OR one special character
    """

    def validate(self, password, user=None):
        if password is None:
            raise ValidationError("La contraseña es obligatoria.")

        if len(password) != 8:
            raise ValidationError("La contraseña debe tener exactamente 8 caracteres.")

        # Must contain at least one uppercase
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Debe contener al menos una letra mayúscula.")

        # Must contain at least one digit OR one special character
        has_digit = re.search(r"\d", password) is not None
        has_special = re.search(r"[^A-Za-z0-9]", password) is not None
        if not (has_digit or has_special):
            raise ValidationError("Debe contener mínimo un número o un carácter especial.")

    def get_help_text(self):
        return (
            "La contraseña debe tener exactamente 8 caracteres, "
            "al menos una mayúscula y mínimo un número o un carácter especial."
        )