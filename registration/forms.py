# registration/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Profile

# Preguntas de seguridad fijas
PREGUNTA_1 = "¿Cuál es el nombre de tu primera mascota?"
PREGUNTA_2 = "¿Cuál es el nombre de tu abuela materna?"

# Formulario para la creación de un nuevo usuario
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    departamento = forms.CharField(max_length=100, required=True, label="Departamento")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")
    respuesta_seguridad_1 = forms.CharField(
        max_length=255, 
        required=True, 
        label=PREGUNTA_1
    )
    respuesta_seguridad_2 = forms.CharField(
        max_length=255, 
        required=True, 
        label=PREGUNTA_2
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email',
            'telefono',
            'departamento',
            'respuesta_seguridad_1',
            'respuesta_seguridad_2',
        )

# --- Formularios para la recuperación de contraseña ---

User = get_user_model()

# Paso 1: Formulario para identificar al usuario por nombre de usuario
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario"
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario no existe.')
        return username

# Paso 2: Formulario para las preguntas de seguridad
class SecurityQuestionsForm(forms.Form):
    respuesta_seguridad_1 = forms.CharField(
        max_length=255, 
        label="¿Cuál es el nombre de tu primera mascota?"
    )
    respuesta_seguridad_2 = forms.CharField(
        max_length=255, 
        label="¿Cuál es el nombre de tu abuela materna?"
    )

# Paso 3: Formulario para el perfil del usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe algo sobre ti...'}),
        }


    
class CustomUserUpdateForm(forms.ModelForm):
    # Campos que el usuario puede actualizar
    username = forms.CharField(max_length=150, label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    first_name = forms.CharField(max_length=150, required=False, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    last_name = forms.CharField(max_length=150, required=False, label="Apellidos", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    email = forms.EmailField(required=True, label="Correo electrónico", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    departamento = forms.CharField(max_length=100, required=True, label="Departamento", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    respuesta_seguridad_1 = forms.CharField(max_length=255, required=True, label="¿Cuál es el nombre de tu primera mascota?", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    respuesta_seguridad_2 = forms.CharField(max_length=255, required=True, label="¿Cuál es el nombre de tu abuela materna?", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'departamento', 'respuesta_seguridad_1', 'respuesta_seguridad_2']
    
    # La validación para el email se mantiene igual
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige uno diferente.")
        return email