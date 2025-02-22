from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import SparePart, SparePartPhoto, MaintenanceHistory
from .forms import SparePartForm, SparePartPhotoFormSet, CalibrationHistoryForm, MaintenanceHistoryForm, MaintenancePhotoFormSet, UploadCSVForm, SparePartFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import csv
import tablib
from django.utils.text import slugify
import datetime
from django.db.models import Q

@login_required
def spare_part_list(request):
    spare_parts = SparePart.objects.all()
    return render(request, 'spare_parts/spare_part_list.html', {'spare_parts': spare_parts})

@login_required
def spare_part_detail(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk)
    return render(request, 'spare_parts/spare_part_detail.html', {'spare_part': spare_part})

@login_required
def spare_part_create(request):
    if request.method == 'POST':
        form = SparePartForm(request.POST, request.FILES)
        photo_formset = SparePartPhotoFormSet(request.POST, request.FILES)

        if form.is_valid() and photo_formset.is_valid():
            spare_part = form.save(commit=False)
            spare_part.created_by = request.user
            spare_part.updated_by = request.user
            spare_part.save()

            photo_formset.instance = spare_part
            photo_formset.save()
            messages.success(request, 'Spare Part created successfully.')

            return redirect('spare_parts:spare_part_detail', pk=spare_part.pk)
        else:
           messages.error(request, 'There was an error creating the Spare Part.')
    else:
        form = SparePartForm()
        photo_formset = SparePartPhotoFormSet()
    return render(request, 'spare_parts/spare_part_form.html', {'form': form, 'photo_formset': photo_formset, 'action': 'Create'})

@login_required
def spare_part_update(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        form = SparePartForm(request.POST, request.FILES, instance=spare_part)
        photo_formset = SparePartPhotoFormSet(request.POST, request.FILES, instance=spare_part)

        if form.is_valid() and photo_formset.is_valid():
            spare_part = form.save(commit=False)
            spare_part.updated_by = request.user
            spare_part.save()

            photo_formset.save() # This will update/delete existing photos and create new ones

            messages.success(request, 'Spare Part updated successfully.')
            return redirect('spare_parts:spare_part_detail', pk=spare_part.pk)
        else:
            messages.error(request, 'There was an error updating the Spare Part.')
    else:
        form = SparePartForm(instance=spare_part)
        photo_formset = SparePartPhotoFormSet(instance=spare_part)
    return render(request, 'spare_parts/spare_part_form.html', {'form': form, 'spare_part': spare_part, 'photo_formset': photo_formset, 'action': 'Update'})

@login_required
def spare_part_delete(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        spare_part.delete()
        messages.success(request, 'Spare Part deleted successfully.')
        return redirect('spare_parts:spare_part_list')
    return render(request, 'spare_parts/spare_part_confirm_delete.html', {'spare_part': spare_part})

@login_required
def maintenance_history_create(request, spare_part_pk):
    spare_part = get_object_or_404(SparePart, pk=spare_part_pk)
    if request.method == 'POST':
        maintenance_form = MaintenanceHistoryForm(request.POST)
        photo_formset = MaintenancePhotoFormSet(request.POST, request.FILES)

        if maintenance_form.is_valid() and photo_formset.is_valid():
            maintenance_history = maintenance_form.save(commit=False)
            maintenance_history.spare_part = spare_part
            maintenance_history.save()

            photo_formset.instance = maintenance_history
            photo_formset.save()

            messages.success(request, 'Maintenance History created successfully.')
            return redirect('spare_parts:spare_part_detail', pk=spare_part.pk)
        else:
             messages.error(request, 'There was an error creating the Maintenance History.')
    else:
        maintenance_form = MaintenanceHistoryForm()
        photo_formset = MaintenancePhotoFormSet()

    return render(request, 'spare_parts/maintenance_history_form.html', {
        'maintenance_form': maintenance_form,
        'photo_formset': photo_formset,
        'spare_part': spare_part,
        'action': 'Create Maintenance History'
    })

@login_required
def maintenance_history_update(request, pk):
     maintenance_history = get_object_or_404(MaintenanceHistory, pk=pk)
     if request.method == 'POST':
          maintenance_form = MaintenanceHistoryForm(request.POST, instance=maintenance_history)
          photo_formset = MaintenancePhotoFormSet(request.POST, request.FILES, instance=maintenance_history)
          if maintenance_form.is_valid() and photo_formset.is_valid():
               maintenance_history = maintenance_form.save()
               photo_formset.save()

               messages.success(request, 'Maintenance History updated successfully.')
               return redirect('spare_parts:spare_part_detail', pk=maintenance_history.spare_part.pk)
          else:
               messages.error(request, 'There was an error updating the Maintenance History.')

     else:
          maintenance_form = MaintenanceHistoryForm(instance=maintenance_history)
          photo_formset = MaintenancePhotoFormSet(instance=maintenance_history)

     return render(request, 'spare_parts/maintenance_history_form.html', {
          'maintenance_form': maintenance_form,
          'photo_formset': photo_formset,
          'spare_part': maintenance_history.spare_part,
          'maintenance_history': maintenance_history,
          'action': 'Update Maintenance History'
     })
@login_required
def maintenance_history_delete(request, pk):
    maintenance_history = get_object_or_404(MaintenanceHistory, pk=pk)
    spare_part_pk = maintenance_history.spare_part.pk  # Store spare_part_pk before deletion
    if request.method == 'POST':
        maintenance_history.delete()
        messages.success(request, 'Maintenance History deleted successfully.')
        return redirect('spare_parts:spare_part_detail', pk=spare_part_pk)
    return render(request, 'spare_parts/maintenance_history_confirm_delete.html', {'maintenance_history': maintenance_history})

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Check if it's a CSV file
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not a CSV file')
                return redirect('spare_parts:upload_csv')

            data = tablib.Dataset().load(csv_file.read().decode('utf-8'), format='csv')
            errors = []
            success_count = 0

            for index, row in enumerate(data):
                # Skip header row
                if index == 0:
                    continue

                try:
                    spare_part_data = {
                        'name': row[0] or '',
                        'serial_number': row[1] or '',
                        'part_number': row[2] or '',
                        'description': row[3] or '',
                        'section': row[4] or '',
                        'quantity': row[5] or None,
                        'shelf_number': row[6] or '',
                        'shelf_level': row[7] or '',
                        'box_number': row[8] or '',
                        'min_stock_level': row[9] or None,
                        'pr_number': row[10] or '',
                        # 'position_rack': row[11] or '',
                        'status': row[11] or '',
                        'manufacturer': row[12] or '',
                        'model_number': row[13] or '',
                    }

                    form = SparePartForm(spare_part_data)
                    if form.is_valid():
                        spare_part = form.save(commit=False)
                        spare_part.created_by = request.user
                        spare_part.updated_by = request.user
                        spare_part.save()
                        success_count += 1
                    else:
                        errors.append(f"Row {index + 1}: {form.errors.as_text()}")

                except Exception as e:
                    errors.append(f"Row {index + 1}: An unexpected error occurred - {str(e)}")

            if errors:
                messages.error(request, f"Successfully imported {success_count} records.  Errors occurred during import:")
                for error in errors:
                    messages.error(request, error)
            else:
                messages.success(request, f"Successfully imported {success_count} spare parts from CSV.")

            return redirect('spare_parts:spare_part_list')  # Redirect to list view
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UploadCSVForm()
    return render(request, 'spare_parts/upload_csv.html', {'form': form})

from django.http import FileResponse
import io
import datetime
@login_required
def download_csv_template(request):
    # Create a sample dataset
    data = tablib.Dataset(headers=[
        'name', 'serial_number', 'part_number', 'description', 'section', 'quantity',
        'shelf_number', 'shelf_level', 'box_number', 'min_stock_level', 'pr_number',
        'status', 'manufacturer', 'model_number'
    ])

    # Add a sample row
    data.append([
        'Sample Spare Part', 'SN12345', 'PN67890', 'Description of spare part', 'Communication', 10,
        'Shelf 1', 'Level A', 'Box 5', 2, 'PR-2024-001', 'Operational',
        'Manufacturer ABC', 'Model XYZ'
    ])

    # Convert the data to CSV
    csv_data = data.export('csv')

    # Create a file-like buffer to receive CSV data
    buffer = io.BytesIO()
    buffer.write(csv_data.encode('utf-8'))
    buffer.seek(0)

    # Create the HTTP response
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="spare_parts_template.csv"'

    return response

@login_required
def spare_part_list(request):
    spare_parts = SparePart.objects.all()
    query = request.GET.get('q')  # Get the search query from the request

    if query:
        spare_parts = spare_parts.filter(
            Q(name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(part_number__icontains=query) |
            Q(description__icontains=query) |
            Q(tag_id__icontains=query) |
            Q(pr_number__icontains=query) |
            Q(manufacturer__icontains=query) |
            Q(model_number__icontains=query)
        )

    filter_form = SparePartFilterForm(request.GET)
    if filter_form.is_valid():
        section = filter_form.cleaned_data.get('section')
        location = filter_form.cleaned_data.get('location')
        shelf_number = filter_form.cleaned_data.get('shelf_number')
        shelf_level = filter_form.cleaned_data.get('shelf_level')
        box_number = filter_form.cleaned_data.get('box_number')
        status = filter_form.cleaned_data.get('status')

        if section:
            spare_parts = spare_parts.filter(section=section)
        if location:
            spare_parts = spare_parts.filter(location=location)
        if shelf_number:
            spare_parts = spare_parts.filter(shelf_number__icontains=shelf_number)
        if shelf_level:
            spare_parts = spare_parts.filter(shelf_level__icontains=shelf_level)
        if box_number:
            spare_parts = spare_parts.filter(box_number__icontains=box_number)
        if status:
            spare_parts = spare_parts.filter(status=status)


    return render(request, 'spare_parts/spare_part_list.html', {'spare_parts': spare_parts, 'query': query, 'filter_form': filter_form})
