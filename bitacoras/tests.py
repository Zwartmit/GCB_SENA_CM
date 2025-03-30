from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Bitacora
from accounts.models import ApprenticeProfile, InstructorProfile
import tempfile

User = get_user_model()

class BitacorasTests(TestCase):
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
        
        instructor_profile = InstructorProfile.objects.create(
            user=self.instructor
        )
        instructor_profile.linked_apprentices.add(self.apprentice)
        
        # Create test bitacora
        test_file = SimpleUploadedFile(
            "test_bitacora.txt",
            b"This is a test bitacora file.",
            content_type="text/plain"
        )
        
        self.bitacora = Bitacora.objects.create(
            apprentice=self.apprentice,
            file=test_file,
            filename="test_bitacora.txt",
            description="Test bitacora description"
        )

    def test_bitacora_list_view_for_apprentice(self):
        self.client.login(username='apprentice_test', password='Test@12345')
        response = self.client.get(reverse('bitacoras:list_bitacoras'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bitacoras/list_bitacoras.html')
        self.assertContains(response, 'test_bitacora.txt')

    def test_bitacora_upload_view(self):
        self.client.login(username='apprentice_test', password='Test@12345')
        response = self.client.get(reverse('bitacoras:upload_bitacora'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bitacoras/upload_bitacora.html')

    def test_instructor_access_to_apprentice_bitacoras(self):
        self.client.login(username='instructor_test', password='Test@12345')
        response = self.client.get(reverse('bitacoras:apprentice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bitacoras/apprentice_list.html')
        self.assertContains(response, 'Test Apprentice')

    def tearDown(self):
        # Delete test files
        self.bitacora.delete()
