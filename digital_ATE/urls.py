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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
