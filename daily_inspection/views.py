from django.shortcuts import render, get_object_or_404
from .models import InspectionIdent

def inspection_list(request):
    inspections = InspectionIdent.objects.all().order_by('-initiated_at')
    return render(request, 'daily_inspection/inspection_list.html', {'inspections': inspections})

def inspection_detail(request, inspection_id):
    inspection = get_object_or_404(InspectionIdent, inspection_ident=inspection_id)
    return render(request, 'daily_inspection/inspection_detail.html', {'inspection': inspection})