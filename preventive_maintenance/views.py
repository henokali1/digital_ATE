from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PreventiveMaintenance
from .forms import PreventiveMaintenanceForm

# List View
@login_required
def maintenance_list(request):
    records = PreventiveMaintenance.objects.all()
    return render(request, 'preventive_maintenance/list.html', {'records': records})

# Create View
# @login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = PreventiveMaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.logged_by = request.user
            maintenance.save()
            return redirect('maintenance_list')
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
            return redirect('maintenance_list')
    else:
        form = PreventiveMaintenanceForm(instance=maintenance)
    return render(request, 'preventive_maintenance/form.html', {'form': form})


# Delete View
@login_required
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(PreventiveMaintenance, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        return redirect('maintenance_list')
    return render(request, 'preventive_maintenance/confirm_delete.html', {'maintenance': maintenance})
