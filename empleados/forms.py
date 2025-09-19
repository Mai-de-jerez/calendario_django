# empleados/forms.py
from django import forms
from .models import Empleado, Departamento
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.exceptions import ObjectDoesNotExist


class EmpleadoForm(forms.ModelForm):
    # Campo de texto para que el usuario escriba el nombre del departamento
    departamento_nombre = forms.CharField(
        label="Departamento",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Empleado
        fields = ['nombre', 'apellidos', 'telefono', 'email', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'observaciones': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="default"),
        }
    

    def clean(self):
        """
        Método de validación principal para el formulario.
        Se usa para validar datos que dependen de múltiples campos.
        """
        cleaned_data = super().clean()
        
        # Validar la existencia del departamento
        departamento_nombre = cleaned_data.get('departamento_nombre')
        if departamento_nombre:
            try:
                # Intenta encontrar el departamento, ignorando mayúsculas/minúsculas
                self.departamento_instance = Departamento.objects.get(nombre__iexact=departamento_nombre)
            except ObjectDoesNotExist:
                # Si no existe, lanza un error de validación
                self.add_error('departamento_nombre', "El departamento no existe.")

        # Obtener los datos para la validación de duplicados
        nombre = cleaned_data.get('nombre')
        apellidos = cleaned_data.get('apellidos')

        # Comprobar si existe un empleado con el mismo nombre y apellidos
        if nombre and apellidos:
            queryset = Empleado.objects.filter(
                nombre__iexact=nombre,
                apellidos__iexact=apellidos,
            )

            # Si el formulario está en modo de edición, excluye la instancia actual del chequeo
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                # Si se encuentra un duplicado, lanza un error de validación para todo el formulario
                raise forms.ValidationError(
                    "¡Ya existe un empleado con ese nombre y apellidos! No pueden existir dos empleados con el mismo nombre y apellidos."
                )

        return cleaned_data


    # Sobreescribe el método save() para asignar el departamento al empleado antes de guardar
    def save(self, commit=True):
        empleado = super().save(commit=False)
        empleado.departamento = self.departamento_instance
        if commit:
            empleado.save()
        return empleado
    
class EmpleadoUpdateForm(EmpleadoForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Comprueba si el formulario tiene una instancia de un empleado existente
        if self.instance and self.instance.departamento:
            # Si la tiene, rellena el campo 'departamento_nombre' con el nombre del departamento
            self.initial['departamento_nombre'] = self.instance.departamento.nombre