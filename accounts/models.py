from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('apprentice', 'Aprendiz'),
        ('instructor', 'Instructor'),
    )
    
    DOCUMENT_TYPE_CHOICES = (
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('ce', 'Cédula de Extranjería'),
        ('passport', 'Pasaporte'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="El número de teléfono debe tener más de 9 dígitos."
        )
    ])
    
    def __str__(self):
        return f"{self.get_user_type_display()}: {self.username}"

class ApprenticeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='apprentice_profile')
    training_program = models.CharField(max_length=100, verbose_name="Programa de Formación")
    record_number = models.CharField(max_length=20, verbose_name="Número de Ficha")
    linked_company = models.CharField(max_length=100, verbose_name="Empresa Vinculada")
    school_stage_start = models.DateField(verbose_name="Inicio Etapa Lectiva")
    productive_stage_start = models.DateField(verbose_name="Inicio Etapa Productiva")
    
    def __str__(self):
        return f"Perfil de Aprendiz: {self.user.username}"

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    linked_apprentices = models.ManyToManyField( User, related_name='assigned_instructors', blank=True, limit_choices_to={'user_type': 'apprentice'}, verbose_name="Aprendices Vinculados")
    
    def __str__(self):
        return f"Perfil de Instructor: {self.user.username}"
