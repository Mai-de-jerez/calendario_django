# empleados/models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class Departamento(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    apellidos = models.CharField(verbose_name="Apellidos", max_length=100)
    departamento = models.ForeignKey(
        'Departamento', 
        on_delete=models.CASCADE, 
        related_name='empleados',
        verbose_name="Departamento"
    )

    
    telefono = models.CharField(
        verbose_name="Teléfono", 
        max_length=20
    )
    email = models.EmailField(
        verbose_name="Correo electrónico"
    )
   
    observaciones = CKEditor5Field(
        verbose_name="Observaciones",
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        # Ordenación por nombre y apellidos
        ordering = ['nombre', 'apellidos']

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
