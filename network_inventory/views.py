from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import NetworkInventory
from .forms import NetworkInventoryForm
from django.db.models import Q
import csv
from django.http import HttpResponse
from django.conf import settings  # Import settings
import os
from django.contrib.auth.decorators import login_required


@login_required
def network_inventory_list(request):
    network_inventory_items = NetworkInventory.objects.all()

    # Search functionality
    search_term = request.GET.get('search', '')  # Set default to empty string
    if search_term:
        network_inventory_items = network_inventory_items.filter(
            Q(name__icontains=search_term) | Q(ip__icontains=search_term) | Q(manufacturer__icontains=search_term)
        )

    # Filter functionality
    section = request.GET.get('section')
    if section:
        network_inventory_items = network_inventory_items.filter(section=section)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(network_inventory_items, 10)  # Show 10 items per page
    try:
        network_inventory_items = paginator.page(page)
    except PageNotAnInteger:
        network_inventory_items = paginator.page(1)
    except EmptyPage:
        network_inventory_items = paginator.page(paginator.num_pages)

    return render(request, 'network_inventory/network_inventory_list.html', {
        'network_inventory_items': network_inventory_items,
        'section_choices': NetworkInventory.SECTION_CHOICES,
        'search_term': search_term,
        'selected_section': section,
        'current_page': page,
    })


@login_required
def network_inventory_detail(request, pk):
    network_inventory_item = get_object_or_404(NetworkInventory, pk=pk)
    page = request.GET.get('page')
    search_term = request.GET.get('search')
    section = request.GET.get('section')

    return render(request, 'network_inventory/network_inventory_detail.html', {
        'network_inventory_item': network_inventory_item,
        'page': page,
        'search_term': search_term,
        'selected_section': section,
    })


@login_required
def network_inventory_create(request):
    if request.method == 'POST':
        form = NetworkInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Network Inventory item created successfully.')
            return redirect('network_inventory:network_inventory_list')
        else:
             messages.error(request, 'There was an error creating the network inventory item.')
    else:
        form = NetworkInventoryForm()
    return render(request, 'network_inventory/network_inventory_form.html', {'form': form})


@login_required
def network_inventory_update(request, pk):
    network_inventory_item = get_object_or_404(NetworkInventory, pk=pk)
    if request.method == 'POST':
        form = NetworkInventoryForm(request.POST, instance=network_inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Network Inventory item updated successfully.')
            return redirect('network_inventory:network_inventory_list')
    else:
        form = NetworkInventoryForm(instance=network_inventory_item)
    return render(request, 'network_inventory/network_inventory_form.html', {'form': form})


@login_required
def network_inventory_delete(request, pk):
    network_inventory_item = get_object_or_404(NetworkInventory, pk=pk)
    if request.method == 'POST':
        network_inventory_item.delete()
        messages.success(request, 'Network Inventory item deleted successfully.')
        return redirect('network_inventory:network_inventory_list')
    return render(request, 'network_inventory/network_inventory_confirm_delete.html', {'network_inventory_item': network_inventory_item})


@login_required
def network_inventory_import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return redirect('network_inventory:network_inventory_list')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                try:
                    # Map CSV columns to model fields.  Adjust as needed
                    name = row.get('name')
                    ip = row.get('ip')
                    section = row.get('section')
                    manufacturer = row.get('manufacturer')
                    mac_address = row.get('mac_address')
                    remarks = row.get('remarks')

                    if not name or not ip or not section:
                        messages.error(request, f"Skipping row due to missing required fields: {row}")
                        continue

                    # Create the NetworkInventory object
                    NetworkInventory.objects.create(
                        name=name,
                        ip=ip,
                        section=section,
                        manufacturer=manufacturer,
                        mac_address=mac_address,
                        remarks=remarks,
                    )
                except Exception as e:
                    messages.error(request, f"Error importing row: {row} - {e}")

            messages.success(request, 'CSV data imported successfully.')
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {e}')

        return redirect('network_inventory:network_inventory_list')
    return render(request, 'network_inventory/network_inventory_import.html')


@login_required
def network_inventory_download_sample_csv(request):
     file_path = os.path.join(settings.BASE_DIR, 'network_inventory', 'static', 'network_inventory', 'sample_network_inventory.csv')
     if os.path.exists(file_path):
         with open(file_path, 'rb') as fh:
             response = HttpResponse(fh.read(), content_type="text/csv")
             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
             return response
     raise Http404
