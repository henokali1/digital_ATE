# preventive_maintenance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PreventiveMaintenance
from .forms import PreventiveMaintenanceForm
from job_card.models import JobCard
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from location.models import Location
from asset.models import Asset
from django.contrib.auth.models import User
from django.db.models import Q




# List View
@login_required
def maintenance_list(request):
    records = PreventiveMaintenance.objects.all().order_by('-start_date')

    # Retrieve filter values from request
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    section_filter = request.GET.get('section')
    location_filter = request.GET.get('location')
    asset_filter = request.GET.get('asset')
    completed_by_filter = request.GET.get('completed_by')

    # Filtering logic
    if start_date_filter and end_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            records = records.filter(start_date__range=[start_date, end_date])
        except (ValueError, TypeError):
            pass  # Ignore if a bad date value is supplied
    elif start_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            records = records.filter(start_date__gte=start_date)
        except (ValueError, TypeError):
            pass
    elif end_date_filter:
        try:
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            records = records.filter(start_date__lte=end_date)
        except (ValueError, TypeError):
            pass

    if section_filter:
        records = records.filter(section=section_filter)
    if location_filter:
        records = records = records.filter(location_id=location_filter)
    if asset_filter:
        records = records.filter(asset__id=asset_filter).distinct()  # distinct to avoid duplicates
    if completed_by_filter:
        records = records.filter(completed_by__id=completed_by_filter).distinct()  # distinct to avoid duplicates


    per_page = int(request.GET.get('per_page', 10))  # Get the per_page value or set to default 10

    # Pagination
    paginator = Paginator(records, per_page)
    page = request.GET.get('page', 1)
    try:
        maintenances = paginator.page(page)
    except PageNotAnInteger:
        maintenances = paginator.page(1)
    except EmptyPage:
        maintenances = paginator.page(paginator.num_pages)

    # Prepare filter options for the template
    sections = PreventiveMaintenance.SECTION_CHOICES
    locations = Location.objects.all()
    assets = Asset.objects.all()
    completed_by_users = User.objects.all()

    context = {
        'records': maintenances,
        'per_page': per_page,
        'sections': sections,
        'locations': locations,
        'assets': assets,
        'completed_by_users': completed_by_users,
        'start_date_filter': start_date_filter,  # Pass the filter values to the template
        'end_date_filter': end_date_filter,
        'section_filter': section_filter,
        'location_filter': location_filter,
        'asset_filter': asset_filter,
        'completed_by_filter': completed_by_filter,

    }

    return render(request, 'preventive_maintenance/list.html', context)



# Create View
@login_required
def maintenance_create(request):
    try:
        jc_id = request.GET.get('jc')
        job_card = None
    except:
        jc_id = None
        job_card = None
    
    if jc_id:
        try:
            job_card = get_object_or_404(JobCard, id=jc_id)  # Fetch the JobCard instance
        except:
            job_card = None


    if request.method == 'POST':
        form = PreventiveMaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.logged_by = request.user
            maintenance.save()
            form.save_m2m()
            
            # Link the PreventiveMaintenance to the JobCard
            if job_card:
                job_card.preventive_maintenance_id = maintenance
                job_card.save()
                return redirect('/job_card/')

            records = PreventiveMaintenance.objects.all().order_by('-logged_at')
            per_page = int(request.GET.get('per_page', 10))
            paginator = Paginator(records, per_page)
            page = request.GET.get('page', 1)
            try:
                maintenances = paginator.page(page)
            except PageNotAnInteger:
                maintenances = paginator.page(1)
            except EmptyPage:
                maintenances = paginator.page(paginator.num_pages)
            return render(request, 'preventive_maintenance/list.html', {'records': maintenances, 'per_page': per_page})
    else:
        if job_card:
             form = PreventiveMaintenanceForm(initial={'task_description': job_card.task_description})
        else:
            form = PreventiveMaintenanceForm()
    return render(request, 'preventive_maintenance/form.html', {'form': form})


# Update View
@login_required
def maintenance_update(request, pk):
    maintenance = get_object_or_404(PreventiveMaintenance, pk=pk)
    if request.method == 'POST':
        form = PreventiveMaintenanceForm(request.POST, request.FILES, instance=maintenance)
        if form.is_valid():
            form.save()
            records = PreventiveMaintenance.objects.all()
            return render(request, 'preventive_maintenance/list.html', {'records': records})
    else:
        form = PreventiveMaintenanceForm(instance=maintenance)
    return render(request, 'preventive_maintenance/form.html', {'form': form})


# Delete View
@login_required
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(PreventiveMaintenance, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        records = PreventiveMaintenance.objects.all()
        return render(request, 'preventive_maintenance/list.html', {'records': records})
    return render(request, 'preventive_maintenance/confirm_delete.html', {'maintenance': maintenance})

@login_required
def maintenance_detail(request, pk):
    maintenance = get_object_or_404(PreventiveMaintenance, pk=pk)
    return render(request, 'preventive_maintenance/detail.html', {'maintenance': maintenance})
