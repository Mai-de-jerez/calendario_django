from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Evento, Lugar 
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import EventoForm, EventoUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q

# Create your views here.

class OwnerOrSuperuserRequiredMixin(AccessMixin):
    """
    Mixin que comprueba si el usuario es un superusuario o el creador del objeto.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Obtiene el objeto para verificar la propiedad
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

        # Comprueba si el usuario es superusuario o el creador del objeto
        if not (request.user.is_superuser or obj.creador == request.user):
            # Redirige a una página de acceso denegado o a la lista de eventos
            return redirect('eventos:evento_list')
            
        return super().dispatch(request, *args, **kwargs)

class EventoListView(ListView):
    """
    Vista para mostrar una lista de todos los eventos.
    """
    model = Evento
    paginate_by = 10 # Número de eventos por página

    def get_queryset(self):
        # 1. Obtenemos el conjunto de datos inicial
        queryset = super().get_queryset()

        # 2. Inicializamos un diccionario vacío para los filtros
        filtros = {}

        # 3. Verificamos cada posible parámetro de la URL
        responsable_query = self.request.GET.get('responsable', '')
        lugar_query = self.request.GET.get('lugar', '')
        modulo_query = self.request.GET.get('modulo', '')

        # 4. Construimos los filtros solo si tienen un valor
        if responsable_query:
            # Usamos Q para el filtro OR en nombre y apellido
            queryset = queryset.filter(
                Q(responsable__nombre__icontains=responsable_query) |
                Q(responsable__apellidos__icontains=responsable_query)
            )

        if lugar_query:
            # Filtro por nombre de lugar
            filtros['lugar__nombre__icontains'] = lugar_query

        if modulo_query:
            # Filtro por nombre de módulo (Many-to-Many)
            filtros['modulo__nombre__icontains'] = modulo_query
            
        # 5. Aplicamos los filtros restantes (si los hay)
        queryset = queryset.filter(**filtros)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos todas las consultas a la plantilla para que los campos no se vacíen
        context['responsable_query'] = self.request.GET.get('responsable', '')
        context['lugar_query'] = self.request.GET.get('lugar', '')
        context['modulo_query'] = self.request.GET.get('modulo', '')
        return context

class EventoDetailView(DetailView):
    """
    Vista para mostrar los detalles de un solo evento.
    """
    model = Evento

    
class EventoCreate(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('eventos:evento_list') + '?ok'


class EventoUpdate(OwnerOrSuperuserRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse_lazy('eventos:evento_list') + '?ok'
        

class EventoDelete(OwnerOrSuperuserRequiredMixin, DeleteView):
    model = Evento
    
    def get_success_url(self):
        return reverse_lazy('eventos:evento_list') + '?ok'

# Vista de la API para el calendario
class EventoApiView(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        
        eventos_formateados = []
        for evento in eventos:
            eventos_formateados.append({
                'title': evento.titulo,
                # Usamos .isoformat() para formatear las fechas y horas correctamente
                'start': f"{evento.fecha.isoformat()}T{evento.hora_inicio.isoformat()}",
                'end': f"{evento.fecha.isoformat()}T{evento.hora_fin.isoformat()}",
                'url': reverse('eventos:evento_detail', args=[evento.pk])
            })
        
        return JsonResponse(eventos_formateados, safe=False)

# Vista para el calendario (renderiza la plantilla)
class CalendarioView(TemplateView):
    template_name = 'eventos/calendario.html'