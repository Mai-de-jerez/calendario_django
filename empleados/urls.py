from django.urls import path
from .views import EmpleadoListView, EmpleadoDetailView, EmpleadoCreate, EmpleadoUpdate, EmpleadoDelete

empleados_patterns = ([
    path('', EmpleadoListView.as_view(), name='empleados'),
    path('<int:pk>/', EmpleadoDetailView.as_view(), name='empleado'),
    path('create/', EmpleadoCreate.as_view(), name='create'),
    path('update/<int:pk>/', EmpleadoUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', EmpleadoDelete.as_view(), name='delete')
], 'empleados')