from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import timedelta
from empleados.models import Empleado

# Obtenemos el modelo de usuario personalizado que has definido
User = get_user_model()

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Lugares"

    def __str__(self):
        return self.nombre

class Modulo(models.Model):
    """
    Modelo para gestionar los módulos de los eventos.
    """
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Evento(models.Model):
    """
    Modelo para gestionar los eventos.
    """
    # Campo de texto para el título del evento
    titulo = models.CharField(max_length=255)
    
    # El responsable es un empleado (usuario) existente
    responsable = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='eventos_responsable')
    
    # El lugar debe ser uno de los lugares registrados
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='eventos_lugar')
    
    # El módulo debe ser uno de los módulos registrados
    modulo = models.ManyToManyField(Modulo, related_name='eventos_modulo')
    
    # Campo de texto largo para la descripción del evento
    descripcion = models.TextField(blank=True)
    
    # Campos para la fecha y hora del evento
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    # Campo que guarda el usuario que creó este evento
    creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='eventos_creados'
    )
    
    class Meta:
        ordering = ['fecha', 'hora_inicio']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f'{self.titulo} - {self.fecha}'

