from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, F
from django.utils import timezone
from .models import DashboardItem
from .forms import DashboardItemForm


def _gather_stats():
    from job_card.models import JobCard
    from preventive_maintenance.models import PreventiveMaintenance
    from corrective_maintenance.models import CorrectiveMaintenance
    from daily_inspection.models import InspectionIdent, DailyInspection
    from asset.models import Asset
    from spare_parts.models import SparePart

    today = timezone.now().date()
    this_month_start = today.replace(day=1)

    jc_pending      = JobCard.objects.filter(status='Pending').count()
    jc_in_progress  = JobCard.objects.filter(status='In Progress').count()
    jc_on_hold      = JobCard.objects.filter(status='On Hold').count()
    jc_overdue      = JobCard.objects.filter(due_date__lt=today).exclude(status__in=['Completed', 'Rejected']).count()
    jc_unack        = JobCard.objects.filter(acknowledged=False).exclude(status__in=['Completed', 'Rejected']).count()
    jc_high         = JobCard.objects.filter(priority_level='High').exclude(status__in=['Completed', 'Rejected']).count()
    jc_completed_mo = JobCard.objects.filter(status='Completed', completed_at__date__gte=this_month_start).count()

    ppm_this_month  = PreventiveMaintenance.objects.filter(start_date__gte=this_month_start).count()
    ppm_hours_month = round(PreventiveMaintenance.objects.filter(start_date__gte=this_month_start).aggregate(t=Sum('duration'))['t'] or 0, 1)

    cm_this_month   = CorrectiveMaintenance.objects.filter(start_date__gte=this_month_start).count()
    cm_hours_month  = round(CorrectiveMaintenance.objects.filter(start_date__gte=this_month_start).aggregate(t=Sum('duration'))['t'] or 0, 1)
    cm_by_type      = list(CorrectiveMaintenance.objects.filter(start_date__gte=this_month_start).values('type').annotate(count=Count('id')).order_by('-count'))

    def _shift_stats(ident):
        if not ident:
            return {'inspected': 0, 'total': 0, 'pct': 0}
        total     = DailyInspection.objects.filter(inspection_ident=ident).count()
        inspected = DailyInspection.objects.filter(inspection_ident=ident).exclude(status__isnull=True).exclude(status='').count()
        return {'inspected': inspected, 'total': total, 'pct': round(inspected / total * 100, 1) if total else 0}

    day_ident   = InspectionIdent.objects.filter(initiated_at__date=today, shift='DAY').order_by('-initiated_at').first()
    night_ident = InspectionIdent.objects.filter(initiated_at__date=today, shift='NIGHT').order_by('-initiated_at').first()

    latest_insp = InspectionIdent.objects.order_by('-initiated_at').first()
    insp_counts = {}
    if latest_insp:
        for row in DailyInspection.objects.filter(inspection_ident=latest_insp).values('status').annotate(n=Count('id')):
            insp_counts[row['status']] = row['n']

    return {
        'jc_pending': jc_pending, 'jc_in_progress': jc_in_progress,
        'jc_on_hold': jc_on_hold, 'jc_overdue': jc_overdue,
        'jc_unack': jc_unack, 'jc_high': jc_high,
        'jc_completed_mo': jc_completed_mo,
        'ppm_this_month': ppm_this_month, 'ppm_hours_month': ppm_hours_month,
        'cm_this_month': cm_this_month, 'cm_hours_month': cm_hours_month,
        'cm_by_type': cm_by_type,
        'day_stats': _shift_stats(day_ident),
        'night_stats': _shift_stats(night_ident),
        'latest_insp': latest_insp,
        'latest_insp_id': latest_insp.inspection_ident if latest_insp else None,
        'insp_counts': insp_counts,
        'asset_total': Asset.objects.count(),
        'asset_in_use': Asset.objects.filter(status='In Use').count(),
        'asset_spare': Asset.objects.filter(status='Spare').count(),
        'asset_maint': Asset.objects.filter(status='Under Maintenance').count(),
        'asset_unsvc': Asset.objects.filter(status='Unserviceable').count(),
        'sp_out': SparePart.objects.filter(quantity=0).count(),
        'sp_low': SparePart.objects.filter(quantity__gt=0, min_stock_level__isnull=False, quantity__lt=F('min_stock_level')).count(),
        'sp_unsvc': SparePart.objects.filter(status='Unserviceable').count(),
        'today': today,
        'this_month': today.strftime('%B %Y'),
    }


@login_required
def stats_dashboard(request):
    from logbook.models import LogEntry
    from corrective_maintenance.models import CorrectiveMaintenance
    from job_card.models import JobCard

    stats = _gather_stats()
    recent_logs = LogEntry.objects.select_related('location').prefetch_related('initials').order_by('-logged_at')[:5]
    recent_cm   = CorrectiveMaintenance.objects.select_related('location').order_by('-logged_at')[:5]
    recent_jc   = JobCard.objects.select_related('location', 'created_by').order_by('-created_at')[:5]
    context = {**stats, 'recent_logs': recent_logs, 'recent_cm': recent_cm, 'recent_jc': recent_jc}
    return render(request, 'admin_dashboard/stats_dashboard.html', context)


@login_required
def api_stats(request):
    stats = _gather_stats()
    # Make JSON-serialisable (remove ORM objects)
    stats.pop('latest_insp', None)
    stats.pop('today', None)
    stats.pop('this_month', None)
    return JsonResponse(stats)


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
