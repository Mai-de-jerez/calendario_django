from django.contrib import admin
from .models import Empleado, Departamento

# Register your models here.
class DepartamentoAdmin(admin.ModelAdmin):
    # Esto le dice a Django que busque en el campo 'nombre' para el autocompletado
    search_fields = ['nombre']


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    autocomplete_fields = ['departamento']

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)