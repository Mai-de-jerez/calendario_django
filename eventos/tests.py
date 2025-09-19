# eventos/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta
from .models import Evento, Lugar, Modulo
from empleados.models import Empleado, Departamento
from .forms import EventoForm, EventoUpdateForm

User = get_user_model()

class EventoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear usuario staff
        cls.staff_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass',
            is_staff=True
        )

        # Crear otro usuario
        cls.other_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='userpass',
            is_staff=False
        )

        # Crear departamento y empleado
        cls.depto = Departamento.objects.create(nombre="IT")
        cls.empleado = Empleado.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            departamento=cls.depto,
            telefono="123456789",
            email="juan.perez@example.com",
        )

        # Crear lugar y módulo
        cls.lugar = Lugar.objects.create(nombre="Sala 1")
        cls.modulo1 = Modulo.objects.create(nombre="Modulo A")
        cls.modulo2 = Modulo.objects.create(nombre="Modulo B")

        # Crear evento existente
        cls.evento = Evento.objects.create(
            titulo="Evento Test",
            descripcion="Descripción prueba",
            fecha=date.today(),
            hora_inicio=time(10, 0),
            hora_fin=time(12, 0),
            responsable=cls.empleado,
            lugar=cls.lugar,
            creador=cls.staff_user
        )
        cls.evento.modulo.set([cls.modulo1, cls.modulo2])

    def setUp(self):
        self.client = Client()

    # ------------------
    # Tests de modelos
    # ------------------
    def test_str_methods(self):
        self.assertEqual(str(self.lugar), "Sala 1")
        self.assertEqual(str(self.modulo1), "Modulo A")
        self.assertEqual(str(self.evento), f"Evento Test - {self.evento.fecha}")

    def test_evento_ordering(self):
        e2 = Evento.objects.create(
            titulo="Segundo Evento",
            descripcion="Otro evento",
            fecha=date.today(),
            hora_inicio=time(9, 0),
            hora_fin=time(10, 0),
            responsable=self.empleado,
            lugar=self.lugar,
            creador=self.staff_user
        )
        eventos = list(Evento.objects.all())
        self.assertEqual(eventos, [e2, self.evento])  # Orden por fecha y hora_inicio

    # ------------------
    # Tests de formularios
    # ------------------
    def test_form_valid(self):
        """Verifica que el formulario es válido y que los objetos son creados correctamente."""
        data = {
            'titulo': "Nuevo Evento",
            'descripcion': "Descripcion",
            'fecha': date.today(),
            'hora_inicio': "14:00",
            'hora_fin': "15:00",
            'responsable_nombre': "Juan",
            'responsable_apellidos': "Pérez",
            'lugar_nombre': "Sala 1",
            'modulo_nombres': "Modulo A, Modulo B"
        }
        form = EventoForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

        # Ahora el formulario maneja todo en una sola llamada
        evento = form.save(creador=self.staff_user)
        
        # Verificar las asignaciones
        self.assertEqual(evento.responsable, self.empleado)
        self.assertEqual(evento.lugar, self.lugar)
        
        # La relación Many-to-Many ya debería estar guardada
        self.assertEqual(
            set(evento.modulo.values_list('nombre', flat=True)),
            {"Modulo A", "Modulo B"}
        )  
    
    def test_form_invalid_lugar(self):
        data = {
            'titulo': "Evento Fail",
            'descripcion': "",
            'fecha': date.today(),
            'hora_inicio': "14:00",
            'hora_fin': "15:00",
            'responsable_nombre': "Juan",
            'responsable_apellidos': "Pérez",
            'lugar_nombre': "NoExiste",
            'modulo_nombres': "Modulo A"
        }
        form = EventoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('lugar_nombre', form.errors)

    def test_form_overlap_event(self):
        data = {
            'titulo': "Evento Superpuesto",
            'descripcion': "",
            'fecha': self.evento.fecha,
            'hora_inicio': "11:00",
            'hora_fin': "13:00",
            'responsable_nombre': "Juan",
            'responsable_apellidos': "Pérez",
            'lugar_nombre': "Sala 1",
            'modulo_nombres': "Modulo A"
        }
        form = EventoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_hora_inicio_after_fin(self):
        data = {
            'titulo': "Evento Fallo Hora",
            'descripcion': "",
            'fecha': date.today(),
            'hora_inicio': "16:00",
            'hora_fin': "15:00",
            'responsable_nombre': "Juan",
            'responsable_apellidos': "Pérez",
            'lugar_nombre': "Sala 1",
            'modulo_nombres': "Modulo A"
        }
        form = EventoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('hora_fin', form.errors)

    # ------------------
    # Tests de vistas
    # ------------------
    def test_list_view(self):
        response = self.client.get(reverse('eventos:evento_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.evento.titulo)
        self.assertTemplateUsed(response, 'eventos/evento_list.html')

    def test_detail_view(self):
        response = self.client.get(reverse('eventos:evento_detail', args=[self.evento.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.evento.titulo)
        self.assertTemplateUsed(response, 'eventos/evento_detail.html')

    def test_create_view_requires_login(self):
        response = self.client.get(reverse('eventos:evento_create'))
        self.assertEqual(response.status_code, 302)  # Redirige al login

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('eventos:evento_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/evento_form.html')

    def test_update_view_permissions(self):
        # Usuario no creador ni superuser
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('eventos:evento_update', args=[self.evento.pk]))
        self.assertRedirects(response, reverse('eventos:evento_list'))

        # Usuario creador
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('eventos:evento_update', args=[self.evento.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/evento_update_form.html')

    def test_delete_view_permissions(self):
        # Usuario no creador ni superuser
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('eventos:evento_delete', args=[self.evento.pk]))
        self.assertRedirects(response, reverse('eventos:evento_list'))

        # Usuario creador
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('eventos:evento_delete', args=[self.evento.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/evento_confirm_delete.html')

    def test_create_post_view(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'titulo': "Evento Post",
            'descripcion': "Desde post",
            'fecha': date.today(),
            'hora_inicio': "15:00",
            'hora_fin': "16:00",
            'responsable_nombre': "Juan",
            'responsable_apellidos': "Pérez",
            'lugar_nombre': "Sala 1",
            'modulo_nombres': "Modulo A"
        }
        response = self.client.post(reverse('eventos:evento_create'), data)
        self.assertRedirects(response, reverse('eventos:evento_list') + '?ok')
        self.assertTrue(Evento.objects.filter(titulo="Evento Post").exists())

    def test_api_view(self):
        response = self.client.get(reverse('eventos:lista_eventos_api'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{
                'title': self.evento.titulo,
                'start': f"{self.evento.fecha.isoformat()}T{self.evento.hora_inicio.isoformat()}",
                'end': f"{self.evento.fecha.isoformat()}T{self.evento.hora_fin.isoformat()}",
                'url': reverse('eventos:evento_detail', args=[self.evento.pk])
            }]
        )


