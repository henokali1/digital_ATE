# preventive_maintenance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PreventiveMaintenance
from .forms import PreventiveMaintenanceForm
from job_card.models import JobCard
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




# List View
@login_required
def maintenance_list(request):
    records = PreventiveMaintenance.objects.all()

    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')  # Get date filters from query parameters

    #Filtering logic
    if start_date_filter and end_date_filter:
         try:
             start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
             end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
             records = records.filter(start_date__range=[start_date,end_date])
         except (ValueError, TypeError):
               pass #Ignore if a bad date value is supplied
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
    per_page = int(request.GET.get('per_page', 10)) # Get the per_page value or set to default 10
      # Pagination
    paginator = Paginator(records, per_page)
    page = request.GET.get('page', 1)
    try:
       maintenances = paginator.page(page)
    except PageNotAnInteger:
        maintenances = paginator.page(1)
    except EmptyPage:
        maintenances = paginator.page(paginator.num_pages)

    return render(request, 'preventive_maintenance/list.html', {'records': maintenances, 'per_page': per_page})


# Create View
# @login_required
def maintenance_create(request):
    try:
        jc_id = request.GET.get('jc')
        job_card = None
    except:
        jc_id = None
        job_card = None
    
    if jc_id:
        job_card = get_object_or_404(JobCard, id=jc_id)  # Fetch the JobCard instance


    if request.method == 'POST':
        form = PreventiveMaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.logged_by = request.user
            maintenance.save()
            # Now save the many-to-many data
            form.save_m2m()

            # Link the PreventiveMaintenance to the JobCard
            if job_card:
                job_card.preventive_maintenance_id = maintenance
                job_card.save()
                return redirect('/job_card/')

            records = PreventiveMaintenance.objects.all()
            return render(request, 'preventive_maintenance/list.html', {'records': records})
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
