
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, EmailForm, ForgotPasswordForm
from unittest.mock import patch


# Obtener el modelo de usuario personalizado
User = get_user_model()

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)

# Create your tests here.
class RegistrationTests(TestCase):

    def setUp(self):
        # Crear un cliente de prueba
        self.client = Client()
        
        # Datos para crear un usuario de prueba
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'telefono': '123456789',
            'departamento': 'IT',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'respuesta_seguridad_1': 'Milo',
            'respuesta_seguridad_2': 'María'
        }
        
        # Crear el usuario en la base de datos de prueba
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            telefono=self.user_data['telefono'],
            departamento=self.user_data['departamento'],
            password=self.user_data['password1'],
            respuesta_seguridad_1=self.user_data['respuesta_seguridad_1'],
            respuesta_seguridad_2=self.user_data['respuesta_seguridad_2']
        )
        
    # ------------------
    # Tests de modelos
    # ------------------
    def test_customuser_model_creation(self):
        """Verifica que el modelo CustomUser se crea con los campos correctos."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.respuesta_seguridad_1, 'Milo')

    def test_profile_creation_with_signal(self):
        """Verifica que un perfil se crea automáticamente para un nuevo usuario."""
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertFalse(profile.avatar)

    # ------------------
    # Tests de formularios
    # ------------------
    @patch('registration.models.custom_upload_to')
    def test_custom_user_creation_form_is_valid(self, mock_custom_upload_to):
        """Verifica que el formulario de creación de usuario es válido con datos correctos."""
        # Usar username y email únicos para que no choquen con self.user
        data = self.user_data.copy()
        data['username'] = 'uniqueuser'
        data['email'] = 'uniqueuser@example.com'
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_custom_user_creation_form_invalid_email(self):
        """Verifica que el formulario de creación de usuario rechaza un email duplicado."""
        data = self.user_data.copy()
        data['email'] = 'testuser@example.com'  # Email ya en uso
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_form_invalid_duplicate_email(self):
        """Verifica que el formulario de actualización de email rechaza correos duplicados."""
        # Crear un segundo usuario para tener un email duplicado
        User.objects.create_user(username='otheruser', email='other@example.com', password='password')
        # Intentar actualizar el email del usuario de prueba al email del otro usuario
        form = EmailForm(data={'email': 'other@example.com'}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    # ------------------
    # Tests de vistas (URLs y lógica de negocio)
    # ------------------
    def test_signup_view_can_create_user(self):
        """Verifica que la vista de registro puede crear un nuevo usuario."""
        new_user_data = {
            'username': 'anotheruser',
            'email': 'anotheruser@example.com',
            'telefono': '987654321',
            'departamento': 'Finanzas',
            'password1': 'AComplexP@ssw0rd123',
            'password2': 'AComplexP@ssw0rd123',
            'respuesta_seguridad_1': 'Toby',
            'respuesta_seguridad_2': 'Sofía'
        }
        
        response = self.client.post(reverse('signup'), new_user_data)
        
        # Imprimir errores si los hay
        if response.status_code == 200:
            print(response.context['form'].errors)
        
        # Verificar la redirección y la existencia del nuevo usuario
        self.assertRedirects(response, reverse('login') + '?register')
        self.assertTrue(User.objects.filter(username='anotheruser').exists())

    def test_profile_update_view_requires_login(self):
        """Verifica que la vista de perfil redirige si el usuario no está logueado."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_update_view_access(self):
        """Verifica que la vista de perfil funciona para un usuario logueado."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile_form.html')

    def test_password_reset_username_view(self):
        """Verifica el primer paso del restablecimiento de contraseña."""
        response = self.client.get(reverse('password_reset_username'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_username.html')

    def test_password_reset_question_view_success(self):
        """Verifica el flujo exitoso de las preguntas de seguridad."""
        self.client.post(reverse('password_reset_username'), {'username': 'testuser'})
        
        response = self.client.post(reverse('password_reset_question'), {
            'respuesta_seguridad_1': 'Milo',
        }, follow=True)
        
        self.assertRedirects(response, reverse('password_reset_confirm'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')