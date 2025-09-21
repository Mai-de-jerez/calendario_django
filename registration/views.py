# registration/views.py 

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ForgotPasswordForm, ProfileForm, CustomUserUpdateForm


# Obtener el modelo de usuario personalizado
User = get_user_model()

# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Aquí puedes personalizar los widgets de los campos
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de Usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Correo electrónico'})
        form.fields['telefono'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Teléfono'})
        form.fields['departamento'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Departamento'})
        form.fields['respuesta_seguridad_1'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Tu respuesta aquí'})
        form.fields['respuesta_seguridad_2'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Tu respuesta aquí'})

        return form


def password_reset_username(request):
    """
    Paso 1: Solicita el nombre de usuario para iniciar el proceso.
    """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            request.session['temp_username'] = username
            request.session['question_step'] = 1  # Iniciar el paso 1 de las preguntas
            return redirect('password_reset_question')
    else:
        form = ForgotPasswordForm()
        
    return render(request, 'registration/password_reset_username.html', {'form': form})

def password_reset_question(request):
    """
    Paso 2: Muestra las preguntas de seguridad secuencialmente y verifica las respuestas.
    """
    username = request.session.get('temp_username')
    question_step = request.session.get('question_step', 1) 

    if not username:
        messages.error(request, 'No se encontró un usuario para el restablecimiento.')
        return redirect('password_reset_username')
    
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        if question_step == 1:
            respuesta_correcta = (request.POST.get('respuesta_seguridad_1') == user.respuesta_seguridad_1)
            
            if respuesta_correcta:
                request.session.pop('question_step', None) 
                return redirect('password_reset_confirm')
            else:
                messages.error(request, 'Respuesta incorrecta. Por favor, intente con la siguiente pregunta.')
                request.session['question_step'] = 2
                return render(request, 'registration/password_reset_question.html', {'question_step': 2})
        
        elif question_step == 2:
            respuesta_correcta = (request.POST.get('respuesta_seguridad_2') == user.respuesta_seguridad_2)
            
            if respuesta_correcta:
                request.session.pop('question_step', None)
                return redirect('password_reset_confirm')
            else:
                messages.error(request, 'Ha sido imposible verificar su identidad, contacte con un administrador.')
                request.session.flush() 
                return redirect('login')
                
    return render(request, 'registration/password_reset_question.html', {'question_step': question_step})

def password_reset_confirm(request):
    """
    Paso 3: Permite al usuario establecer una nueva contraseña.
    """
    username = request.session.get('temp_username')
    if not username:
        messages.error(request, 'No se encontró un usuario para el restablecimiento.')
        return redirect('password_reset_username')
    
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['temp_username']
            messages.success(request, 'Su contraseña ha sido restablecida exitosamente. Puede iniciar sesión ahora.')
            return redirect('login')
    else:
        form = SetPasswordForm(user)

    return render(request, 'registration/password_reset_confirm.html', {'form': form})

## Creando el perfil de usuario

@login_required
def profile_update(request):
    # Aseguramos que el usuario tenga un objeto de perfil. Si no lo tiene, lo creamos.
    profile_instance, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Instanciamos ambos formularios con los datos enviados por el usuario
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_instance)

        # Validamos los dos formularios
        if user_form.is_valid() and profile_form.is_valid():
            # Si ambos son válidos, guardamos los cambios en la base de datos
            user_form.save()
            profile_form.save()
            messages.success(request, '¡Tu perfil se ha actualizado con éxito! 🎉')
            return redirect('profile')
    else:
        # En una petición GET, llenamos los formularios con los datos actuales del usuario
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_instance)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'registration/profile_form.html', context)
    
    