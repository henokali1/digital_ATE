from django.urls import path
from . import views

app_name = 'feature_request'

urlpatterns = [
    path('', views.feature_request_list, name='feature_request_list'),
    path('create/', views.feature_request_create, name='feature_request_create'),
    path('update/<int:pk>/', views.feature_request_update, name='feature_request_update'),
    path('delete/<int:pk>/', views.feature_request_delete, name='feature_request_delete'),
     path('detail/<int:pk>/', views.feature_request_detail, name='feature_request_detail'), # Detail view
]