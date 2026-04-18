from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset, PositionRack, AssetHistory, CalibrationHistory, CalibrationDocument
from .forms import AssetForm
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import AssetForm, CSVImportForm, AssetHistoryForm
from location.models import Location
from django.db.models import Q
import io

@login_required
def home(request):
    return HttpResponse("Welcome to Digital ATE!")


# List all assets
@login_required
def asset_list(request):
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Base queryset
    queryset = Asset.objects.all()
    
    # Apply search if there's a query
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(tag_id__icontains=search_query) |
            Q(section__icontains=search_query) |
            Q(location__name__icontains=search_query) |
            Q(status__icontains=search_query)
        ).distinct()
    
    # Order by newest first
    queryset = queryset.order_by('-id')
    
    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 items per page
    page = request.GET.get('page', 1)
    
    try:
        assets = paginator.page(page)
    except PageNotAnInteger:
        assets = paginator.page(1)
    except EmptyPage:
        assets = paginator.page(paginator.num_pages)
    
    return render(request, 'asset/asset_list.html', {
        'assets': assets,
        'search_query': search_query,
        'user': request.user
    })


# Create a new asset
@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('asset_list')  # Redirect to the list page after saving
    else:
        form = AssetForm()
    return render(request, 'asset/asset_form.html', {'form': form})

@login_required
def asset_detail(request, id):
    from corrective_maintenance.models import CorrectiveMaintenance
    from preventive_maintenance.models import PreventiveMaintenance
    from daily_inspection.models import DailyInspection
    from django.utils import timezone

    asset = get_object_or_404(Asset, id=id)
    history_form = AssetHistoryForm()

    from django.db.models import Count

    corrective_records  = asset.corrective_maintenances.all().order_by('-start_date')
    preventive_records  = asset.preventive_maintenances.all().order_by('-start_date')
    calibration_records = asset.calibration_history.prefetch_related('documents').all()

    insp_counts = (
        DailyInspection.objects
        .filter(asset=asset)
        .values('status')
        .annotate(count=Count('status'))
        .order_by('status')
    )
    insp_total = sum(item['count'] for item in insp_counts)

    return render(request, 'asset/asset_detail.html', {
        'asset': asset,
        'history_form': history_form,
        'corrective_records':  corrective_records,
        'preventive_records':  preventive_records,
        'calibration_records': calibration_records,
        'insp_counts': insp_counts,
        'insp_total':  insp_total,
        'today': timezone.now().date(),
    })


# Update an existing asset
@login_required
def asset_edit(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'asset/asset_form.html', {'form': form})

@login_required
def asset_delete(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')
    return render(request, 'asset/asset_confirm_delete.html', {'asset': asset})

@login_required
def import_assets(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('import_assets')

            # Read CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(decoded_file))
                
                success_count = 0
                error_count = 0
                errors = []

                for row in csv_data:
                    try:
                        # Get or create related objects
                        try:
                            location = Location.objects.get(name=row['location'])
                        except Location.DoesNotExist:
                            raise ValueError(f"Location '{row['location']}' does not exist")

                        position_rack = None
                        if row.get('position_rack'):
                            position_rack, _ = PositionRack.objects.get_or_create(
                                name=row['position_rack']
                            )

                        # Create asset
                        Asset.objects.create(
                            name=row['name'],
                            serial_number=row['serial_number'],
                            tag_id=row.get('tag_id', ''),  # Optional
                            section=row['section'],
                            location=location,
                            position_rack=position_rack,
                            status=row['status'],
                            manufacturer=row.get('manufacturer', ''),
                            model_number=row.get('model_number', ''),
                            part_number=row.get('part_number', ''),
                            morning_shift_daily_inspection_required=row.get(
                                'morning_shift_daily_inspection_required', 'false').lower() == 'true',
                            night_shift_daily_inspection_required=row.get(
                                'night_shift_daily_inspection_required', 'false').lower() == 'true',
                            preventive_maintenance_required=row.get(
                                'preventive_maintenance_required', 'true').lower() == 'true',
                            corrective_maintenance_required=row.get(
                                'corrective_maintenance_required', 'false').lower() == 'true',
                            remarks=row.get('remarks', ''),
                             installation_date = row.get('installation_date', None)  # Handle installation date
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {csv_data.line_num}: {str(e)}")

                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} assets.')
                if error_count > 0:
                    messages.warning(request, f'Failed to import {error_count} assets.')
                    for error in errors:
                        messages.error(request, error)

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                return redirect('import_assets')

            return redirect('asset_list')
    else:
        form = CSVImportForm()

    return render(request, 'asset/import_assets.html', {'form': form})

@login_required
def download_sample_csv(request):
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_assets.csv"'

    # Create CSV writer
    writer = csv.writer(response)
    
    # Write headers
    writer.writerow([
        'name', 'serial_number', 'tag_id', 'section', 'location', 
        'position_rack', 'status', 'manufacturer', 'model_number', 
        'part_number', 'morning_shift_daily_inspection_required',
        'night_shift_daily_inspection_required', 'preventive_maintenance_required',
        'corrective_maintenance_required', 'remarks', 'installation_date'
    ])
    
    # Write sample data
    writer.writerow([
        'Sample Asset 1', 'SN001', 'TAG-12345678', 'Surveillance', 'Tower',
        'Rack-1', 'In Use', 'Sample Manufacturer', 'Model-123',
        'Part-456', 'true', 'false', 'true', 'false',
        'Sample remarks', '2024-10-26'
    ])

    return response

@login_required
def add_asset_history(request, id):
        asset = get_object_or_404(Asset, id=id)
        if request.method == 'POST':
            history_form = AssetHistoryForm(request.POST, request.FILES)
            if history_form.is_valid():
                history_entry = history_form.save(commit=False)
                history_entry.asset = asset
                history_entry.user = request.user
                history_entry.save()
                messages.success(request, 'Asset history updated.')
                return redirect('asset_detail', id=id)
        else:
            history_form = AssetHistoryForm()

        return render(request, 'asset/asset_detail.html', {'asset': asset, 'history_form': history_form})


@login_required
def add_calibration(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        calibration_date      = request.POST.get('calibration_date', '').strip()
        next_calibration_date = request.POST.get('next_calibration_date', '').strip()
        notes                 = request.POST.get('notes', '').strip()

        if not calibration_date or not next_calibration_date:
            messages.error(request, 'Both calibration date and next calibration date are required.')
            return redirect('asset_detail', id=id)

        calibration = CalibrationHistory.objects.create(
            asset=asset,
            calibration_date=calibration_date,
            next_calibration_date=next_calibration_date,
            notes=notes or None,
            created_by=request.user,
        )
        for doc in request.FILES.getlist('documents'):
            CalibrationDocument.objects.create(
                calibration=calibration,
                document=doc,
                name=doc.name,
            )
        messages.success(request, 'Calibration record added successfully.')
    return redirect('asset_detail', id=id)


@login_required
def delete_calibration(request, calibration_id):
    calibration = get_object_or_404(CalibrationHistory, id=calibration_id)
    asset_id = calibration.asset.id
    if request.method == 'POST':
        calibration.delete()
        messages.success(request, 'Calibration record deleted.')
    return redirect('asset_detail', id=asset_id)


@login_required
def asset_inspections_filtered(request, id, status):
    from daily_inspection.models import DailyInspection
    asset = get_object_or_404(Asset, id=id)
    records = (
        DailyInspection.objects
        .filter(asset=asset, status=status)
        .select_related('inspection_ident')
        .prefetch_related('inspected_by')
        .order_by('-created_at')
    )
    return render(request, 'asset/asset_inspections_filtered.html', {
        'asset': asset,
        'records': records,
        'status': status,
    })


@login_required
def asset_lifecycle_list(request):
    from django.utils import timezone
    today = timezone.now().date()
    assets = Asset.objects.select_related('location', 'position_rack').filter(installation_date__isnull=False).order_by('name')

    # Annotate lifecycle status for sorting: expired first, nearing second, active last
    expired = [a for a in assets if a.lifecycle_status == 'expired']
    nearing  = [a for a in assets if a.lifecycle_status == 'nearing']
    active   = [a for a in assets if a.lifecycle_status == 'active']
    no_data  = Asset.objects.select_related('location').filter(installation_date__isnull=True).order_by('name')

    return render(request, 'asset/asset_lifecycle_list.html', {
        'expired': expired,
        'nearing': nearing,
        'active': active,
        'no_data': no_data,
        'today': today,
        'total': len(expired) + len(nearing) + len(active) + no_data.count(),
    })
