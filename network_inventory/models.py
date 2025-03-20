from django.db import models

class NetworkInventory(models.Model):
    SECTION_CHOICES = [
        ('Communication', 'Communication'),
        ('Navigation', 'Navigation'),
        ('Surveillance', 'Surveillance'),
        ('Aviation Networks', 'Aviation Networks'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    name = models.CharField(max_length=200, verbose_name='Name')
    ip = models.GenericIPAddressField(verbose_name='IP Address')
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, verbose_name='Section')
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='Manufacturer')
    mac_address = models.CharField(max_length=17, blank=True, null=True, verbose_name='MAC Address')
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Network Inventory'  # Correct pluralization in admin
        ordering = ['name']