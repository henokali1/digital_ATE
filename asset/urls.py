from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('create/', views.asset_create, name='asset_create'),
    path('<int:id>/', views.asset_detail, name='asset_detail'),
    path('edit/<int:id>/', views.asset_edit, name='asset_edit'), 
    path('delete/<int:id>/', views.asset_delete, name='asset_delete'),
]
