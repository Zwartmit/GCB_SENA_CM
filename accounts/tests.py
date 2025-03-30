from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ApprenticeProfile, InstructorProfile

User = get_user_model()

class CuentasTest(TestCase):
    def setUp(self):
        # Crear usuarios de prueba
        self.aprendiz = User.objects.create_user(
            username='aprendiz_prueba',
            email='aprendiz@prueba.com',
            password='Prueba@12345',
            user_type='apprentice',
            document_type='cc',
            document_number='1234567890',
            phone_number='1234567890',
            first_name='Prueba',
            last_name='Aprendiz'
        )
        
        self.instructor = User.objects.create_user(
            username='instructor_prueba',
            email='instructor@prueba.com',
            password='Prueba@12345',
            user_type='instructor',
            document_type='cc',
            document_number='0987654321',
            phone_number='0987654321',
            first_name='Prueba',
            last_name='Instructor'
        )
        
        # Crear perfiles
        ApprenticeProfile.objects.create(
            user=self.aprendiz,
            training_program='Programa de Prueba',
            record_number='PP12345',
            linked_company='Empresa de Prueba',
            school_stage_start='2023-01-01',
            productive_stage_start='2023-06-01'
        )
        
        InstructorProfile.objects.create(
            user=self.instructor
        )

    def test_pagina_login(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_pagina_registro(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_aprendiz(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'aprendiz_prueba',
            'password': 'Prueba@12345'
        })
        self.assertRedirects(response, reverse('dashboard:dashboard'))

    def test_login_instructor(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'instructor_prueba',
            'password': 'Prueba@12345'
        })
        self.assertRedirects(response, reverse('dashboard:dashboard'))
