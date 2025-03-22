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
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

@login_required
@require_POST
def save_to_logbook(request):
    try:
        inspection_id = request.POST.get('inspection_id')
        asset_name = request.POST.get('asset_name')
        location_id = request.POST.get('location_id')
        remarks = request.POST.get('remarks')
        
        daily_inspection = get_object_or_404(DailyInspection, id=inspection_id)
        current_time = timezone.localtime()

        # Create log entry
        log_entry = LogEntry.objects.create(
            date=current_time.date(),
            time=current_time.time(),
            location=daily_inspection.asset.location,
            remarks=f"[{asset_name}:] {remarks}" if remarks else f"[{asset_name}] Photo update"
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

@login_required
def inspection_list(request):
    inspections_list = InspectionIdent.objects.all().order_by('-initiated_at')
    per_page = int(request.GET.get('per_page', 10)) # Get the per_page value or set to default 10

    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date') # Get date filters from query parameters

    #Filtering logic
    if start_date_filter and end_date_filter:
         try:
             start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
             end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
             inspections_list = inspections_list.filter(initiated_at__date__range=[start_date,end_date])
         except (ValueError, TypeError):
               pass #Ignore if a bad date value is supplied
    elif start_date_filter:
         try:
             start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
             inspections_list = inspections_list.filter(initiated_at__date__gte=start_date)
         except (ValueError, TypeError):
               pass
    elif end_date_filter:
         try:
             end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
             inspections_list = inspections_list.filter(initiated_at__date__lte=end_date)
         except (ValueError, TypeError):
               pass
    # Pagination
    paginator = Paginator(inspections_list, per_page)
    page = request.GET.get('page', 1)
    try:
        inspections = paginator.page(page)
    except PageNotAnInteger:
        inspections = paginator.page(1)
    except EmptyPage:
        inspections = paginator.page(paginator.num_pages)
    
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
         'per_page': per_page,
    })

@login_required
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
        
        # Update the inspection
        daily_inspection.status = request.POST.get('status')
        daily_inspection.remarks = request.POST.get('remarks') #Update Remarks
        daily_inspection.inspected_at = timezone.now()
        
        # Handle photo upload
        photo = request.FILES.get('photo')
        if photo:
            daily_inspection.photo = photo
        
        daily_inspection.save()
        
        # Add the current user to inspected_by if not already added
        if request.user not in daily_inspection.inspected_by.all():
            daily_inspection.inspected_by.add(request.user)
        
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

@login_required
def filtered_assets(request, inspection_id, status):
    inspection = get_object_or_404(InspectionIdent, inspection_ident=inspection_id)
    filtered_inspections = inspection.daily_inspections.filter(status=status).order_by('asset__position_rack', 'asset__name')

    context = {
        'inspection': inspection,
        'filtered_inspections': filtered_inspections,
        'status': status,
    }
    return render(request, 'daily_inspection/filtered_assets.html', context)
