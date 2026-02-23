from django.contrib import admin
from .models import PasswordResetToken


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'used', 'is_valid')
    list_filter = ('used', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__username', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at')
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = "¿Válido?"
