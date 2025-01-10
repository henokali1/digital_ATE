# logbook/urls.py
from django.urls import path
from . import views

app_name = 'logbook'

urlpatterns = [
    path('', views.log_list, name='log_list'),
    path('new/', views.create_log_entry, name='create_log_entry'), # Create new log entry
    path('<int:pk>/edit/', views.update_log_entry, name='update_log_entry'),  # Edit log entry
    path('<int:pk>/delete/', views.delete_log_entry, name='delete_log_entry'),  # Delete log entry
]