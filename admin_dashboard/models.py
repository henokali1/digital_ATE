from django.db import models

class DashboardItem(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.title
