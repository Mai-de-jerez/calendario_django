from django import forms
from .models import Evento, Empleado, Lugar, Modulo
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class EventoForm(forms.ModelForm):
    """
    Formulario para el modelo Evento con campos de texto para la entrada de
    responsable, lugar y módulo, con validación personalizada.
    """
    responsable_nombre = forms.CharField(
        label="Nombre del responsable",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control autocomplete-field'})
    )
    responsable_apellidos = forms.CharField(
        label="Apellidos del responsable",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control autocomplete-field'})
    )
    lugar_nombre = forms.CharField(
        label="Lugar",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control autocomplete-field'})
    )
   
    # Este campo de texto se usará para agregar los módulos dinámicamente en el frontend
    modulo_nombres = forms.CharField(
        label="Módulos (separar los módulos con comas)",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    fecha = forms.DateField(
        label="Fecha",
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        )
    )


    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha', 'hora_inicio', 'hora_fin']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descripcion': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="default"),
        }
    
    def clean(self):
        """
        Valida que los nombres de los campos de texto existan en la base de datos
        y que no haya duplicados.
        """
        cleaned_data = super().clean()

        # Validación específica para el responsable usando los dos campos
        self.responsable_instance = self.clean_empleado_field(
            cleaned_data.get('responsable_nombre'),
            cleaned_data.get('responsable_apellidos')
        )

        # Validación genérica de los campos de texto para Lugar y Módulo
        self.lugar_instance = self.clean_foreignkey_field(
            'lugar_nombre', cleaned_data, Lugar, "lugar"
        )
        # Validación personalizada para el campo de módulos
        self.modulo_instances = self.clean_modulo_field(cleaned_data.get('modulo_nombres'))

        # Validación de superposición de eventos
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        fecha = cleaned_data.get('fecha')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            self.add_error('hora_fin', "La hora de fin debe ser posterior a la hora de inicio.")
        
        if (self.lugar_instance and fecha and hora_inicio and hora_fin):
            overlapping_events = Evento.objects.filter(
                lugar=self.lugar_instance,
                fecha=fecha
            )
            if self.instance and self.instance.pk:
                overlapping_events = overlapping_events.exclude(pk=self.instance.pk)

            for evento in overlapping_events:
                if not (hora_inicio >= evento.hora_fin or hora_fin <= evento.hora_inicio):
                    raise forms.ValidationError(f"Este evento se superpone con el evento '{evento.titulo}' en día y hora.")
        
        return cleaned_data
    
    def clean_modulo_field(self, modulo_nombres_str):
        """
        Método auxiliar para validar los nombres de los módulos y devolver las instancias.
        """
        if not modulo_nombres_str:
            raise forms.ValidationError("Debe seleccionar al menos un módulo para el evento.")

        modulos = []
        nombres_modulos = [nombre.strip() for nombre in modulo_nombres_str.split(',') if nombre.strip()]

        for nombre in nombres_modulos:
            try:
                modulo_instance = Modulo.objects.get(nombre__iexact=nombre)
                modulos.append(modulo_instance)
            except ObjectDoesNotExist:
                raise forms.ValidationError(f"El módulo '{nombre}' no existe.")
            except MultipleObjectsReturned:
                raise forms.ValidationError(f"Existen múltiples módulos con el nombre '{nombre}'. Por favor, sé más específico.")

        # Devolver un conjunto para evitar duplicados si se han introducido
        return list(set(modulos))

    def clean_empleado_field(self, nombre, apellidos):
        """
        Método auxiliar para validar el campo de responsable buscando por nombre y apellidos.
        """
        if not nombre or not apellidos:
            if not nombre:
                self.add_error('responsable_nombre', "Este campo es obligatorio.")
            if not apellidos:
                self.add_error('responsable_apellidos', "Este campo es obligatorio.")
            return None
        
        try:
            # Busca un empleado por nombre y apellidos, ignorando mayúsculas/minúsculas
            instance = Empleado.objects.get(nombre__iexact=nombre, apellidos__iexact=apellidos)
            return instance
        except ObjectDoesNotExist:
            self.add_error('responsable_nombre', "El empleado no existe. Por favor, asegúrate de que el nombre y los apellidos sean correctos.")
        except MultipleObjectsReturned:
            self.add_error('responsable_nombre', "Existen múltiples empleados con ese nombre y apellidos. Por favor, sé más específico.")
        
        return None

    def clean_foreignkey_field(self, field_name, cleaned_data, model_class, verbose_name):
        """
        Método auxiliar para validar campos de texto que corresponden a ForeignKeys
        buscando solo por el nombre.
        """
        field_value = cleaned_data.get(field_name)
        if not field_value:
            self.add_error(field_name, "Este campo es obligatorio.")
            return None
        
        try:
            instance = model_class.objects.get(nombre__iexact=field_value)
            return instance
        except ObjectDoesNotExist:
            self.add_error(field_name, f"El {verbose_name} no existe.")
        except MultipleObjectsReturned:
            self.add_error(field_name, f"Existen múltiples {verbose_name}s con este nombre. Por favor, sé más específico.")
        
        return None
    

    def save(self, commit=True, creador=None):
        """
        Sobreescribe el método save() para asignar los objetos relacionados
        y el creador antes de guardar el evento.
        """
        evento = super().save(commit=False)
        
        # Asignar el creador si se proporciona
        if creador:
            evento.creador = creador
        
        # Asignar las instancias obtenidas en clean()
        evento.responsable = self.responsable_instance
        evento.lugar = self.lugar_instance
        
        if commit:
            evento.save()
            # Guardar la relación muchos a muchos después de guardar el evento principal
            # Usamos set() para asignar todos los módulos de una vez.
            evento.modulo.set(self.modulo_instances)
            
        return evento
    

class EventoUpdateForm(EventoForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rellena los campos de texto con los valores de la instancia existente
        if self.instance and self.instance.responsable:
            # Ahora rellenamos ambos campos por separado
            self.initial['responsable_nombre'] = self.instance.responsable.nombre
            self.initial['responsable_apellidos'] = self.instance.responsable.apellidos
        if self.instance and self.instance.lugar:
            self.initial['lugar_nombre'] = self.instance.lugar.nombre
        # Para el campo de módulos, debemos unir los nombres en una cadena separada por comas
        if self.instance and self.instance.modulo.exists():
            modulos_nombres = ", ".join([m.nombre for m in self.instance.modulo.all()])
            self.initial['modulo_nombres'] = modulos_nombres
