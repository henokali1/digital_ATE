from django import forms
from .models import DashboardItem

class DashboardItemForm(forms.ModelForm):
    class Meta:
        model = DashboardItem
        fields = ['title', 'url']
