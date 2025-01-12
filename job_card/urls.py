from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_card_list, name='job_card_list'),
    path('new/', views.job_card_create, name='job_card_create'),
    path('<int:pk>/edit/', views.job_card_update, name='job_card_update'),
    path('<int:pk>/delete/', views.job_card_delete, name='job_card_delete'),
]
