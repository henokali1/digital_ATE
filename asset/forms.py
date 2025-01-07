from django import forms
from .models import Asset
from location.models import Location

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'serial_number', 'tag_id', 'section', 'location', 'status', 'photo']
    
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="Select a Location")
