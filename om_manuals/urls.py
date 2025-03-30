from django.urls import path
from . import views

app_name = 'om_manuals'

urlpatterns = [
    path('', views.manual_list, name='manual_list'),
]
