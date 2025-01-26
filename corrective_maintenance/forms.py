from django import forms
from .models import CorrectiveMaintenance
from location.models import Location
from django.contrib.auth.models import User

class CorrectiveMaintenanceForm(forms.ModelForm):
    completed_by = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Maintenance Completed By"
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completed_by'].label_from_instance = self.user_full_name

    def user_full_name(self, user):
      return f'{user.first_name} {user.last_name}'