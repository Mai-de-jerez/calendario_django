# empleados/templatetags/empleados_extras.py
from django import template
from empleados.models import Empleado

register = template.Library()

@register.simple_tag
def get_empleado_list():
    empleados = Empleado.objects.all()
    return empleados