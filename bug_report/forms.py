from django import forms
from .models import BugReport

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['title', 'description', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior', 'severity', 'screenshot', 'comments']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'steps_to_reproduce': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'expected_behavior': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actual_behavior': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'screenshot': forms.FileInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }