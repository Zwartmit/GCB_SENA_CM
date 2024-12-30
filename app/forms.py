from django import forms
from django.forms import inlineformset_factory
from app.models import *

class AprendizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Aprendiz
        fields = ['nombre', 'tipo_documento', 'num_documento', 'correo', 'usuario', 'contrasena', 'num_ficha', 'programa_formacion', 'fecha_inicio_programa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Nombre',
                'required': True,
                'class': 'form-control',
            }),
            'tipo_documento': forms.Select(attrs={
                'placeholder': 'Tipo de documento',
                'required': True,
                'class': 'form-control',
            }),
            'num_documento': forms.NumberInput(attrs={
                'placeholder': 'N° de documento',
                'required': True,
                'class': 'form-control',
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'Correo',
                'required': True,
                'class': 'form-control',
            }),
            'usuario': forms.TextInput(attrs={
                'placeholder': 'Usuario',
                'required': True,
                'class': 'form-control',
            }),
            'contrasena': forms.PasswordInput(attrs={
                'placeholder': 'Contraseña',
                'required': True,
                'class': 'form-control',
            }),
            'num_ficha': forms.NumberInput(attrs={
                'placeholder': 'N° de ficha',
                'required': True,
                'class': 'form-control',
            }),
            'programa_formacion': forms.Select(attrs={
                'placeholder': 'Programa de formación',
                'required': True,
                'class': 'form-control',
            }),
            'fecha_inicio_programa': forms.DateInput(attrs={
                'placeholder': 'Fecha de inicio del programa de formación',
                'required': True,
                'class': 'form-control',
            }),
        }

class InstructorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Aprendiz
        fields = ['nombre', 'tipo_documento', 'num_documento', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Nombre',
                'required': True,
                'class': 'form-control',
            }),
            'tipo_documento': forms.Select(attrs={
                'placeholder': 'Tipo de documento',
                'required': True,
                'class': 'form-control',
            }),
            'num_documento': forms.NumberInput(attrs={
                'placeholder': 'N° de documento',
                'required': True,
                'class': 'form-control',
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'Correo',
                'required': True,
                'class': 'form-control',
            })
        }

class EmpresaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'modalidad', 'jefe', 'num_telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Nombre',
                'required': True,
                'class': 'form-control',
            }),
            'nit': forms.NumberInput(attrs={
                'placeholder': 'NIT',
                'required': True,
                'class': 'form-control',
            }),
            'modalidad': forms.Select(attrs={
                'placeholder': 'Modalidad',
                'required': True,
                'class': 'form-control',
            }),
            'jefe': forms.TextInput(attrs={
                'placeholder': 'Jefe',
                'required': True,
                'class': 'form-control',
            }),
            'num_telefono': forms.NumberInput(attrs={
                'placeholder': 'N° de teléfono',
                'required': True,
                'class': 'form-control',
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'Correo',
                'required': True,
                'class': 'form-control',
            })
        }

BitacoraFormSet = inlineformset_factory(
    Aprendiz,
    DetalleBitacora,
    fields=('bitacora', 'fecha', 'descripcion'),
    widgets={
        'bitacora': forms.Textarea(attrs={
            'placeholder': 'Actividad realizada',
            'required': True,
            'class': 'form-control',
            'rows': 2,
        }),
        'descripcion': forms.Textarea(attrs={
            'placeholder': 'Descripción',
            'required': True,
            'class': 'form-control',
        }),
    },
    extra=1,
    can_delete=True,
)
