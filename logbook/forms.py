# logbook/forms.py
from django import forms
from .models import LogEntry
from location.models import Location


class LogEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['date', 'time', 'location', 'initials', 'photos', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="Select a Location")
