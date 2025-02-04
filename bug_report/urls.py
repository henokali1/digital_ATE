from django.urls import path
from . import views

app_name = 'bug_report'

urlpatterns = [
    path('', views.bug_report_list, name='bug_report_list'),
    path('create/', views.bug_report_create, name='bug_report_create'),
    path('update/<int:pk>/', views.bug_report_update, name='bug_report_update'),
    path('delete/<int:pk>/', views.bug_report_delete, name='bug_report_delete'),
    path('detail/<int:pk>/', views.bug_report_detail, name='bug_report_detail'),
]