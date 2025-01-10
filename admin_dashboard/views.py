from django.shortcuts import render, get_object_or_404, redirect
from .models import DashboardItem
from .forms import DashboardItemForm
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_home(request):
    return render(request, 'admin_dashboard/home.html')

# List and Create Dashboard Items
@login_required
def dashboard_list(request):
    items = DashboardItem.objects.all()

    if request.method == 'POST':
        form = DashboardItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_list')
    else:
        form = DashboardItemForm()

    return render(request, 'admin_dashboard/dashboard_list.html', {'items': items, 'form': form})

# Edit a Dashboard Item
@login_required
def dashboard_edit(request, id):
    item = get_object_or_404(DashboardItem, id=id)
    if request.method == 'POST':
        form = DashboardItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard_list')
    else:
        form = DashboardItemForm(instance=item)

    return render(request, 'admin_dashboard/dashboard_edit.html', {'form': form})

# Delete a Dashboard Item
@login_required
def dashboard_delete(request, id):
    item = get_object_or_404(DashboardItem, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard_list')

    return render(request, 'admin_dashboard/dashboard_delete.html', {'item': item})
