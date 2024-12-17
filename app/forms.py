from django import forms
from django.forms import inlineformset_factory
from app.models import *

class AprendizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Aprendiz
        fields = ['nombre', 'tipo_documento', 'num_documento', 'correo', 'num_ficha', 'programa_formacion', 'fecha_inicio_programa']
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

BitacoraFormSet = inlineformset_factory(
    Aprendiz,
    DetalleBitacora,
    fields=('bitacora', 'fecha', 'descripcion'),
    widgets={
        'bitacora': forms.Textarea(attrs={
            'placeholder': 'Elemento',
            'required': True,
            'class': 'form-control',
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
