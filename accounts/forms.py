from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.validators import RegexValidator
from .models import User, ApprenticeProfile, InstructorProfile
import re

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        max_length=254
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
        strip=False,
    )

class BaseUserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    DOCUMENT_TYPES = [
        ('', '-- Seleccione el tipo de documento --'),
        ('cc', 'Cédula de Ciudadanía'),
        ('ti', 'Tarjeta de Identidad'),
        ('passport', 'Pasaporte'),
    ]
    document_type = forms.ChoiceField(choices=DOCUMENT_TYPES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    document_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="El número de teléfono debe tener más de 9 dígitos."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Ingrese su contraseña deseada.",
    )
    password2 = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'document_type', 'document_number', 
                  'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        return password

class ApprenticeRegisterForm(BaseUserRegisterForm):
    training_program = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    record_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    linked_company = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school_stage_start = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    productive_stage_start = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'apprentice'
        
        if commit:
            user.save()
            apprentice_profile = ApprenticeProfile(
                user=user,
                training_program=self.cleaned_data['training_program'],
                record_number=self.cleaned_data['record_number'],
                linked_company=self.cleaned_data['linked_company'],
                school_stage_start=self.cleaned_data['school_stage_start'],
                productive_stage_start=self.cleaned_data['productive_stage_start']
            )
            apprentice_profile.save()
        
        return user

class InstructorRegisterForm(BaseUserRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'instructor'
        
        if commit:
            user.save()
            instructor_profile = InstructorProfile(user=user)
            instructor_profile.save()
        
        return user
