from django.urls import path
from . import views

urlpatterns = [
    path('inspections/', views.inspection_list, name='inspection_list'),
    path('inspection/<int:inspection_id>/', views.inspection_detail, name='inspection_detail'),
]
