from django.contrib import admin
from .models import Evento, Lugar, Modulo

# Register your models here.
class ModuloAdmin(admin.ModelAdmin):
    # Esto le dice a Django que busque en el campo 'nombre' para el autocompletado
    search_fields = ['nombre']

class LugarAdmin(admin.ModelAdmin):
    # Esto le dice a Django que busque en el campo 'nombre' para el autocompletado
    search_fields = ['nombre']


class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    autocomplete_fields = ['lugar', 'modulo']

admin.site.register(Evento, EventoAdmin)
admin.site.register(Lugar, LugarAdmin)
admin.site.register(Modulo, ModuloAdmin)

