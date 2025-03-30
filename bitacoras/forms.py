from django import forms
from .models import Bitacora

class BitacoraUploadForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = ['file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LinkApprenticeForm(forms.Form):
    apprentice = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="-- Seleccionar Aprendiz --"
    )
    
    def __init__(self, *args, **kwargs):
        instructor = kwargs.pop('instructor', None)
        super(LinkApprenticeForm, self).__init__(*args, **kwargs)
        
        from accounts.models import User
        
        # Obtener todos los aprendices que no están vinculados a este instructor
        if instructor:
            current_linked_ids = instructor.instructor_profile.linked_apprentices.values_list('id', flat=True)
            self.fields['apprentice'].queryset = User.objects.filter(
                user_type='apprentice'
            ).exclude(
                id__in=current_linked_ids
            )
        else:
            self.fields['apprentice'].queryset = User.objects.filter(user_type='apprentice')
