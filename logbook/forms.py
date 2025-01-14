# logbook/forms.py
from django import forms
from .models import LogEntry
from location.models import Location
from django.contrib.auth.models import User


class LogEntryForm(forms.ModelForm):
    initials = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Select Users"
    )
    class Meta:
        model = LogEntry
        fields = ['date', 'time', 'location', 'initials', 'photos', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()
        self.fields['location'].empty_label = "Select a Location"
    # location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="Select a Location")
