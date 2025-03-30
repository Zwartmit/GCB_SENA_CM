from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import ApprenticeProfile, InstructorProfile

User = get_user_model()

class DashboardTests(TestCase):
    def setUp(self):
        # Create test users
        self.apprentice = User.objects.create_user(
            username='apprentice_test',
            email='apprentice@test.com',
            password='Test@12345',
            user_type='apprentice',
            document_type='cc',
            document_number='1234567890',
            phone_number='1234567890',
            first_name='Test',
            last_name='Apprentice'
        )
        
        self.instructor = User.objects.create_user(
            username='instructor_test',
            email='instructor@test.com',
            password='Test@12345',
            user_type='instructor',
            document_type='cc',
            document_number='0987654321',
            phone_number='0987654321',
            first_name='Test',
            last_name='Instructor'
        )
        
        # Create profiles
        ApprenticeProfile.objects.create(
            user=self.apprentice,
            training_program='Test Program',
            record_number='TP12345',
            linked_company='Test Company',
            school_stage_start='2023-01-01',
            productive_stage_start='2023-06-01'
        )
        
        InstructorProfile.objects.create(
            user=self.instructor
        )

    def test_dashboard_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_apprentice_dashboard_access(self):
        self.client.login(username='apprentice_test', password='Test@12345')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        self.assertContains(response, 'Raise blogs')
        self.assertContains(response, 'Consult logbooks')

    def test_instructor_dashboard_access(self):
        self.client.login(username='instructor_test', password='Test@12345')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        self.assertContains(response, 'Link apprentices')
        self.assertContains(response, 'Consult apprentices')
