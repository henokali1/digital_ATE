from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard_home, name='dashboard_home'),
    path('', views.dashboard_list, name='dashboard_list'),
    path('edit/<int:id>/', views.dashboard_edit, name='dashboard_edit'),
    path('delete/<int:id>/', views.dashboard_delete, name='dashboard_delete'),
]
