from django import forms
from .models import PreventiveMaintenance

class PreventiveMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PreventiveMaintenance
        exclude = ['logged_at', 'logged_by']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
