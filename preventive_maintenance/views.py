from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PreventiveMaintenance
from .forms import PreventiveMaintenanceForm
from job_card.models import JobCard


# List View
@login_required
def maintenance_list(request):
    records = PreventiveMaintenance.objects.all()
    return render(request, 'preventive_maintenance/list.html', {'records': records})

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
