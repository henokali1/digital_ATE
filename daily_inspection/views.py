from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from .models import InspectionIdent, DailyInspection
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Count, Q
from .models import InspectionIdent, DailyInspection
from logbook.models import LogEntry
from django.utils.timezone import localtime

@require_POST
def save_to_logbook(request):
    try:
        inspection_id = request.POST.get('inspection_id')
        daily_inspection = get_object_or_404(DailyInspection, id=inspection_id)
        
        current_time = timezone.localtime()
        
        # Create log entry
        log_entry = LogEntry.objects.create(
            date=current_time.date(),
            time=current_time.time(),
            location=daily_inspection.asset.location,
            remarks=f"[{daily_inspection.asset.name}] {daily_inspection.remarks}"
        )
        
        # Add the photo if it exists
        if daily_inspection.photo:
            log_entry.photos = daily_inspection.photo
            
        # Add the current user to the log entry
        log_entry.initials.add(request.user)
        log_entry.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Successfully saved to logbook'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def inspection_list(request):
    inspections = InspectionIdent.objects.all().order_by('-initiated_at')
    
    # Add progress information to each inspection
    for inspection in inspections:
        # Get total count of daily inspections
        total_count = inspection.daily_inspections.count()
        
        # Get count of inspected assets (where status is not null or empty)
        inspected_count = inspection.daily_inspections.exclude(
            Q(status__isnull=True) | Q(status='')
        ).count()
        
        # Calculate percentage
        progress_percentage = (inspected_count / total_count * 100) if total_count > 0 else 0
        
        # Add attributes to the inspection object
        inspection.total_count = total_count
        inspection.inspected_count = inspected_count
        inspection.progress_percentage = progress_percentage

         # Get Status Counts
        status_counts = inspection.daily_inspections.values('status').annotate(count=Count('status'))
        inspection.status_counts = {item['status']: item['count'] for item in status_counts if item['status']}  # Filter out null statuses and put into a dictionary
        
        # Check if an item has not been given a status or if status is null
        pending_count = total_count - inspected_count
        inspection.pending_count = pending_count
     

    return render(request, 'daily_inspection/inspection_list.html', {
        'inspections': inspections,
    })


@require_http_methods(["GET", "POST"])
def inspection_detail(request, inspection_id):
    inspection = get_object_or_404(InspectionIdent, inspection_ident=inspection_id)
    daily_inspections = inspection.daily_inspections.all().order_by('asset__position_rack', 'asset__name')

    # Calculate progress statistics
    total_assets = daily_inspections.count()
    inspected_assets = daily_inspections.exclude(status='').exclude(status__isnull=True).count()
    progress_percentage = (inspected_assets / total_assets * 100) if total_assets > 0 else 0

    if request.method == 'POST':
        inspection_id = request.POST.get('inspection_id')
        daily_inspection = get_object_or_404(DailyInspection, id=inspection_id)
        
        # Get the old remarks to check if they've changed
        old_remarks = daily_inspection.remarks
        new_remarks = request.POST.get('remarks')
        
        # Update the inspection
        daily_inspection.status = request.POST.get('status')
        daily_inspection.remarks = new_remarks
        daily_inspection.inspected_at = timezone.now()
        
        # Handle photo upload
        photo = request.FILES.get('photo')
        if photo:
            daily_inspection.photo = photo
        
        daily_inspection.save()
        
        # Add the current user to inspected_by if not already added
        if request.user not in daily_inspection.inspected_by.all():
            daily_inspection.inspected_by.add(request.user)

        # Create a log entry if there are remarks or photos
        if (new_remarks and new_remarks != old_remarks) or photo:
            current_time = localtime(timezone.now())
            log_entry = LogEntry.objects.create(
                date=current_time.date(),
                time=current_time.time(),
                location=daily_inspection.asset.location,
                remarks=f"[{daily_inspection.asset.name}] {new_remarks}" if new_remarks else f"[{daily_inspection.asset.name}] Photo update"
            )
            
            # Add the photo if available
            if photo:
                log_entry.photos = photo
            
            # Add the current user to the log entry
            log_entry.initials.add(request.user)
            log_entry.save()
        
        # Recalculate progress after update
        inspected_assets = daily_inspections.exclude(status='').exclude(status__isnull=True).count()
        progress_percentage = (inspected_assets / total_assets * 100) if total_assets > 0 else 0
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Inspection updated successfully',
                'timestamp': timezone.now().strftime('%d %b %Y %H:%M'),
                'progress': {
                    'inspected': inspected_assets,
                    'total': total_assets,
                    'percentage': round(progress_percentage, 1)
                }
            })
        
        messages.success(request, 'Inspection updated successfully.')
        return redirect('inspection_detail', inspection_id=inspection.inspection_ident)

    context = {
        'inspection': inspection,
        'daily_inspections': daily_inspections,
        'total_assets': total_assets,
        'inspected_assets': inspected_assets,
        'progress_percentage': progress_percentage
    }
    
    return render(request, 'daily_inspection/inspection_detail.html', context)
