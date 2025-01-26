# preventive_maintenance/forms.py
from django import forms
from .models import PreventiveMaintenance
from django.contrib.auth.models import User

class PreventiveMaintenanceForm(forms.ModelForm):
    completed_by = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Maintenance Completed By"
    )
    class Meta:
        model = PreventiveMaintenance
        exclude = ['logged_at', 'logged_by']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
