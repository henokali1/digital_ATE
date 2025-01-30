from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('create/', views.asset_create, name='asset_create'),
    path('<int:id>/', views.asset_detail, name='asset_detail'),
    path('history/<int:id>/add/', views.add_asset_history, name='add_asset_history'),
    path('edit/<int:id>/', views.asset_edit, name='asset_edit'),
    path('delete/<int:id>/', views.asset_delete, name='asset_delete'),
    path('import/', views.import_assets, name='import_assets'),
    path('download-sample-csv/', views.download_sample_csv, name='download_sample_csv'),
]
