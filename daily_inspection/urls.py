from django.urls import path
from . import views

urlpatterns = [
    path('inspections/', views.inspection_list, name='inspection_list'),
    path('inspection/<int:inspection_id>/', views.inspection_detail, name='inspection_detail'),
    path('save-to-logbook/', views.save_to_logbook, name='save_to_logbook'),
    path('inspections/<int:inspection_id>/filtered/<str:status>/', views.filtered_assets, name='filtered_assets'),
]
