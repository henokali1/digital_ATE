from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manifest.json', views.manifest, name='manifest'),
    path('sw.js', views.service_worker, name='service_worker'),
]
