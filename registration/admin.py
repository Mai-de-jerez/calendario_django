from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Sobrescribimos add_form para usar un formulario que incluya 'email'
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'telefono', 'departamento')}),
        ('Preguntas de Seguridad', {'fields': ('respuesta_seguridad_1', 'respuesta_seguridad_2')}),
    )

    # El formulario de edición de un usuario ya existente
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal Adicional', {'fields': ('telefono', 'departamento')}),
        ('Preguntas de Seguridad', {'fields': ('respuesta_seguridad_1', 'respuesta_seguridad_2')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

