from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_control

def home(request):
    return render(request, 'pages/home.html')

@cache_control(max_age=86400)
def manifest(request):
    return render(request, 'pages/manifest.json',
                  content_type='application/manifest+json')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def service_worker(request):
    return render(request, 'pages/sw.js',
                  content_type='application/javascript')
