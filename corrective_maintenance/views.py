# corrective_maintenance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CorrectiveMaintenance
from .forms import CorrectiveMaintenanceForm
from job_card.models import JobCard
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# corrective_maintenance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CorrectiveMaintenance
from .forms import CorrectiveMaintenanceForm
from job_card.models import JobCard
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from location.models import Location
from django.contrib.auth.models import User
from asset.models import Asset

# List View
@login_required
def maintenance_list(request):
    records = CorrectiveMaintenance.objects.all().order_by('-start_date')

    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    type_filter = request.GET.get('type')
    section_filter = request.GET.get('section')
    location_filter = request.GET.get('location')
    completed_by_filter = request.GET.get('completed_by')
    asset_filter = request.GET.get('asset')

    # Date Filtering
    if start_date_filter and end_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            records = records.filter(start_date__range=[start_date, end_date])
        except (ValueError, TypeError):
            pass
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

    # Type Filtering
    if type_filter:
        records = records.filter(type=type_filter)

    # Section Filtering
    if section_filter:
        records = records.filter(section=section_filter)

    # Location Filtering
    if location_filter:
        records = records.filter(location_id=location_filter)  #Filter using the id

    # Completed By Filtering
    if completed_by_filter:
        records = records.filter(completed_by__id=completed_by_filter) #Filter using the id

    # Asset Filtering
    if asset_filter:
        records = records.filter(asset__id=asset_filter)  #Filter using the id


    per_page = int(request.GET.get('per_page', 10))

    # Pagination
    paginator = Paginator(records, per_page)
    page = request.GET.get('page', 1)
    try:
        maintenances = paginator.page(page)
    except PageNotAnInteger:
        maintenances = paginator.page(1)
    except EmptyPage:
        maintenances = paginator.page(paginator.num_pages)

    context = {
        'records': maintenances,
        'per_page': per_page,
        'type_choices': CorrectiveMaintenance.TYPE_CHOICES,
        'section_choices': CorrectiveMaintenance.SECTION_CHOICES,
        'locations': Location.objects.all(),
        'completed_by_users': User.objects.filter(userprofile__ate_staff=True),
        'assets': Asset.objects.all(),
    }

    return render(request, 'corrective_maintenance/list.html', context)

# Create View
@login_required
def maintenance_create(request):
    jc_id = request.GET.get('jc')
    job_card = None
    initial_data = {}  # Initialize an empty dictionary for initial data

    if jc_id:
        job_card = get_object_or_404(JobCard, id=jc_id)  # Fetch the JobCard instance
        initial_data['task_description'] = job_card.task_description  # Populate the initial data

    if request.method == 'POST':
        form = CorrectiveMaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.logged_by = request.user
            maintenance.save()  # Save the main instance first
            form.save_m2m()  # Then, save the many-to-many data
            # Now save the many-to-many data

            # Link the CorrectiveMaintenance to the JobCard
            if job_card:
                job_card.corrective_maintenance_id = maintenance
                job_card.save()
                return redirect('/job_card/')
            return redirect('maintenance_list')
    else:
        form = CorrectiveMaintenanceForm(initial=initial_data)  # Pass the initial data to the form
    return render(request, 'corrective_maintenance/form.html', {'form': form})

# Update View
@login_required
def maintenance_update(request, pk):
    maintenance = get_object_or_404(CorrectiveMaintenance, pk=pk)
    if request.method == 'POST':
        form = CorrectiveMaintenanceForm(request.POST, request.FILES, instance=maintenance)
        if form.is_valid():
            maintenance = form.save()
            form.save_m2m()
            return redirect('maintenance_list')
    else:
        form = CorrectiveMaintenanceForm(instance=maintenance)
    return render(request, 'corrective_maintenance/form.html', {'form': form})

# Delete View
@login_required
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(CorrectiveMaintenance, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        return redirect('maintenance_list')
    return render(request, 'corrective_maintenance/confirm_delete.html', {'object': maintenance})

@login_required
def maintenance_detail(request, pk):
    record = get_object_or_404(CorrectiveMaintenance, pk=pk)
    return render(request, 'corrective_maintenance/detail.html', {'record': record})
