from django.urls import path
from . import views

urlpatterns = [
    path('', views.stats_dashboard, name='stats_dashboard'),
    path('api/', views.api_stats, name='api_stats'),
    path('items/', views.dashboard_list, name='dashboard_list'),
    path('edit/<int:id>/', views.dashboard_edit, name='dashboard_edit'),
    path('delete/<int:id>/', views.dashboard_delete, name='dashboard_delete'),
]
