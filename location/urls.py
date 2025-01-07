from django.urls import path
from . import views

urlpatterns = [
    path('', views.location_list, name='location_list'),
    path('create/', views.location_create, name='location_create'),
    path('update/<int:pk>/', views.location_update, name='location_update'),
    path('delete/<int:pk>/', views.location_delete, name='location_delete'),
]
