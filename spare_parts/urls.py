from django.urls import path
from . import views

app_name = 'spare_parts'

urlpatterns = [
    path('', views.spare_part_list, name='spare_part_list'),
    path('<int:pk>/', views.spare_part_detail, name='spare_part_detail'),
    path('create/', views.spare_part_create, name='spare_part_create'),
    path('<int:pk>/update/', views.spare_part_update, name='spare_part_update'),
    path('<int:pk>/delete/', views.spare_part_delete, name='spare_part_delete'),
    path('<int:spare_part_pk>/maintenance/create/', views.maintenance_history_create, name='maintenance_history_create'),
    path('maintenance/<int:pk>/update/', views.maintenance_history_update, name='maintenance_history_update'),
    path('maintenance/<int:pk>/delete/', views.maintenance_history_delete, name='maintenance_history_delete'),
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    path('download/csv_template/', views.download_csv_template, name='download_csv_template'),
]