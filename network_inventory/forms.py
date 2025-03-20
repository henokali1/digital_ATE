from django import forms
from .models import NetworkInventory

class NetworkInventoryForm(forms.ModelForm):
    class Meta:
        model = NetworkInventory
        fields = ['name', 'ip', 'section', 'manufacturer', 'mac_address', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),  # Adjust rows as needed
        }
