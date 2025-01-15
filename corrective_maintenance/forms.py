from django import forms
from .models import CorrectiveMaintenance
from location.models import Location
from django.contrib.auth.models import User

class CorrectiveMaintenanceForm(forms.ModelForm):
    completed_by = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Select Users"
    )
    class Meta:
        model = CorrectiveMaintenance
        exclude = ['logged_at', 'logged_by', 'duration']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
