from django.contrib import admin
from django.urls import path, include
from asset import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/', include('accounts.urls')), 
    path('asset/', include('asset.urls')),
    path('location/', include('location.urls')),
    path('dashboard/', include('admin_dashboard.urls')),
    path('logbook/', include('logbook.urls')),
    path('preventive_maintenance/', include('preventive_maintenance.urls')),
    path('corrective_maintenance/', include('corrective_maintenance.urls')),
    path('job_card/', include('job_card.urls')),
    path('', include('daily_inspection.urls')),
    path('select2/', include('django_select2.urls')),
    path('bug_report/', include('bug_report.urls')),
    path('feature_requests/', include('feature_request.urls')),
    path('spare_parts/', include('spare_parts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
