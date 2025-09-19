# empleados/views.py
from django.urls import reverse_lazy
from .models import Empleado, Departamento
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EmpleadoForm, EmpleadoUpdateForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Q



class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.
class EmpleadoListView(ListView):
    model = Empleado
    paginate_by = 10 # Número de empleados por página

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Obtenemos los valores de la URL
        busqueda_query = self.request.GET.get('busqueda', '') # Nuevo campo de búsqueda
        departamento_query = self.request.GET.get('departamento', '')
        
        # Aplicamos el filtro de búsqueda combinado para nombre y apellidos
        if busqueda_query:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda_query) |
                Q(apellidos__icontains=busqueda_query)
            )
        
        # Aplicamos el filtro de departamento si existe
        if departamento_query:
            queryset = queryset.filter(departamento__nombre__icontains=departamento_query)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos las variables de búsqueda al contexto para que los campos no se vacíen
        context['busqueda_query'] = self.request.GET.get('busqueda', '')
        context['departamento_query'] = self.request.GET.get('departamento', '')
        return context

class EmpleadoDetailView(DetailView):
    model = Empleado

@method_decorator(staff_member_required, name="dispatch")
class EmpleadoCreate(CreateView):
    model = Empleado
    form_class =EmpleadoForm
   
    def get_success_url(self):
        return reverse_lazy('empleados:empleados') + '?ok'

@method_decorator(staff_member_required, name="dispatch")
class EmpleadoUpdate(UpdateView):
    model = Empleado
    form_class =EmpleadoUpdateForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        # Redirige a la URL de la ficha individual, usando el pk y el slug del objeto.
        return reverse_lazy('empleados:empleados') + '?ok'
    

@method_decorator(staff_member_required, name="dispatch")   
class EmpleadoDelete(DeleteView):
    model = Empleado

    def get_success_url(self):
        return reverse_lazy('empleados:empleados') + '?ok'

