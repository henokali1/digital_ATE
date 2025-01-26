from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_card_list, name='job_card_list'),
    path('new/', views.job_card_create, name='job_card_create'),
    path('<int:pk>/', views.job_card_detail, name='job_card_detail'),
    path('<int:pk>/edit/', views.job_card_update, name='job_card_update'),
    path('<int:pk>/delete/', views.job_card_delete, name='job_card_delete'),
    path('<int:pk>/acknowledge/', views.job_card_acknowledge, name='job_card_acknowledge'),
    path('<int:pk>/update-status/', views.job_card_update_status, name='job_card_update_status'),
    path('<int:pk>/add-remark-to-logbook/', views.job_card_add_remark_to_logbook, name='job_card_add_remark_to_logbook'),
]