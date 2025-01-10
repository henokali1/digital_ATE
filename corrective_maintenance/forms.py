from django import forms
from .models import CorrectiveMaintenance

class CorrectiveMaintenanceForm(forms.ModelForm):
    class Meta:
        model = CorrectiveMaintenance
        exclude = ['logged_at', 'logged_by', 'duration']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
