from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from .models import InspectionIdent, DailyInspection

def inspection_list(request):
    inspections = InspectionIdent.objects.all().order_by('-initiated_at')
    return render(request, 'daily_inspection/inspection_list.html', {'inspections': inspections})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .models import InspectionIdent, DailyInspection

@require_http_methods(["GET", "POST"])
def inspection_detail(request, inspection_id):
    inspection = get_object_or_404(InspectionIdent, inspection_ident=inspection_id)
    daily_inspections = inspection.daily_inspections.all().order_by('asset__position_rack', 'asset__name')

    if request.method == 'POST':
        inspection_id = request.POST.get('inspection_id')
        daily_inspection = get_object_or_404(DailyInspection, id=inspection_id)
        
        # Update the inspection
        daily_inspection.status = request.POST.get('status')
        daily_inspection.remarks = request.POST.get('remarks')
        daily_inspection.inspected_at = timezone.now()
        
        # Handle photo upload
        if request.FILES.get('photo'):
            daily_inspection.photo = request.FILES['photo']
        
        daily_inspection.save()
        
        # Add the current user to inspected_by if not already added
        if request.user not in daily_inspection.inspected_by.all():
            daily_inspection.inspected_by.add(request.user)
        
        messages.success(request, 'Inspection updated successfully.')
        return redirect('inspection_detail', inspection_id=inspection.inspection_ident)

    return render(request, 'daily_inspection/inspection_detail.html', {
        'inspection': inspection,
        'daily_inspections': daily_inspections,
    })