from django import forms
from .models import PreventiveMaintenance

class PreventiveMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PreventiveMaintenance
        exclude = ['logged_at', 'logged_by']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
