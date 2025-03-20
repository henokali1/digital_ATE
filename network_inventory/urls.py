from django.urls import path
from . import views

app_name = 'network_inventory'  # helps in namespacing the urls

urlpatterns = [
    path('', views.network_inventory_list, name='network_inventory_list'),
    path('<int:pk>/', views.network_inventory_detail, name='network_inventory_detail'),
    path('create/', views.network_inventory_create, name='network_inventory_create'),
    path('update/<int:pk>/', views.network_inventory_update, name='network_inventory_update'),
    path('delete/<int:pk>/', views.network_inventory_delete, name='network_inventory_delete'),
    path('import/csv/', views.network_inventory_import_csv, name='network_inventory_import_csv'),
    path('download/sample_csv/', views.network_inventory_download_sample_csv, name='network_inventory_download_sample_csv'),
]