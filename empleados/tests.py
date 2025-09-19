# empleados/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Departamento, Empleado
from .forms import EmpleadoForm, EmpleadoUpdateForm

User = get_user_model()


class EmpleadosTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Usuario staff
        cls.staff_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass',
            is_staff=True
        )

        # Departamento
        cls.depto = Departamento.objects.create(nombre="IT")

        # Empleado de prueba
        cls.empleado = Empleado.objects.create(
            nombre="Juan",
            apellidos="Pérez",
            departamento=cls.depto,
            telefono="123456789",
            email="juan.perez@example.com",
            observaciones="Empleado de pruebas"
        )

    def setUp(self):
        self.client = Client()

    # ------------------
    # Tests de modelos
    # ------------------
    def test_departamento_str(self):
        self.assertEqual(str(self.depto), "IT")

    def test_empleado_str(self):
        self.assertEqual(str(self.empleado), "Juan Pérez")

    def test_empleado_ordering(self):
        e2 = Empleado.objects.create(
            nombre="Ana",
            apellidos="Gómez",
            departamento=self.depto,
            telefono="987654321",
            email="ana.gomez@example.com"
        )
        empleados = list(Empleado.objects.all())
        self.assertEqual(empleados, [e2, self.empleado])  # Orden: Gómez antes que Pérez

    # ------------------
    # Tests de formularios
    # ------------------
    def test_empleado_form_valid(self):
        data = {
            'nombre': 'Carlos',
            'apellidos': 'Lopez',
            'departamento_nombre': 'IT',
            'telefono': '111222333',
            'email': 'carlos.lopez@example.com',
            'observaciones': 'Nuevo empleado'
        }
        form = EmpleadoForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        empleado = form.save()
        self.assertEqual(empleado.departamento, self.depto)

    def test_empleado_form_invalid_departamento(self):
        data = {
            'nombre': 'Carlos',
            'apellidos': 'Lopez',
            'departamento_nombre': 'NoExiste',
            'telefono': '111222333',
            'email': 'carlos.lopez@example.com',
            'observaciones': 'Nuevo empleado'
        }
        form = EmpleadoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('departamento_nombre', form.errors)

    def test_empleado_form_duplicate_name(self):
        data = {
            'nombre': 'Juan',
            'apellidos': 'Pérez',
            'departamento_nombre': 'IT',
            'telefono': '111222333',
            'email': 'duplicado@example.com',
            'observaciones': ''
        }
        form = EmpleadoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_empleado_update_form_initial_departamento(self):
        form = EmpleadoUpdateForm(instance=self.empleado)
        self.assertEqual(form.initial['departamento_nombre'], 'IT')

    # ------------------
    # Tests de vistas
    # ------------------
    def test_empleado_list_view(self):
        response = self.client.get(reverse('empleados:empleados'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'empleados/empleado_list.html')
        self.assertContains(response, self.empleado.nombre)

    def test_empleado_detail_view(self):
        response = self.client.get(reverse('empleados:empleado', args=[self.empleado.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'empleados/empleado_detail.html')
        self.assertContains(response, self.empleado.nombre)

    def test_empleado_create_view_requires_staff(self):
        # Usuario no staff
        self.client.login(username='admin', password='wrongpass')
        response = self.client.get(reverse('empleados:create'))
        self.assertEqual(response.status_code, 302)  # Redirige

        # Usuario staff
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('empleados:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'empleados/empleado_form.html')

    def test_empleado_update_view_requires_staff(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('empleados:update', args=[self.empleado.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'empleados/empleado_update_form.html')

    def test_empleado_delete_view_requires_staff(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('empleados:delete', args=[self.empleado.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'empleados/empleado_confirm_delete.html')

    def test_empleado_create_post(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'nombre': 'Luis',
            'apellidos': 'Martinez',
            'departamento_nombre': 'IT',
            'telefono': '555444333',
            'email': 'luis.martinez@example.com',
            'observaciones': 'Nuevo'
        }
        response = self.client.post(reverse('empleados:create'), data)
        self.assertRedirects(response, reverse('empleados:empleados') + '?ok')
        self.assertTrue(Empleado.objects.filter(nombre='Luis').exists())

    def test_update_empleado_view(self):
        self.client.login(username='admin', password='adminpass')
        update_url = reverse('empleados:update', args=[self.empleado.pk])
        response = self.client.post(update_url, {
            'nombre': 'Juan',
            'apellidos': 'Pérez',
            'telefono': '555555555',
            'email': 'juanmod@example.com',
            'observaciones': 'Actualizado',
            'departamento_nombre': 'IT'
        })
        self.assertRedirects(response, reverse('empleados:empleados') + '?ok')
        self.empleado.refresh_from_db()
        self.assertEqual(self.empleado.telefono, '555555555')
        self.assertEqual(self.empleado.email, 'juanmod@example.com')

    def test_delete_empleado_view(self):
        self.client.login(username='admin', password='adminpass')
        delete_url = reverse('empleados:delete', args=[self.empleado.pk])
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('empleados:empleados') + '?ok')
        self.assertFalse(Empleado.objects.filter(pk=self.empleado.pk).exists())

    def test_list_empleados_pagination(self):
        # Crear varios empleados
        for i in range(10):
            Empleado.objects.create(
                nombre=f'Empleado{i}',
                apellidos='Test',
                departamento=self.depto,
                telefono='0000000',
                email=f'emp{i}@example.com'
            )
        list_url = reverse('empleados:empleados')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['object_list']), 8)  # paginate_by = 8