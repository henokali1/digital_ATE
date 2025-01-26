from django.shortcuts import render, redirect, get_object_or_404
from .forms import LogEntryForm
from .models import Location, LogEntry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, date

@login_required
def create_log_entry(request):
    if request.method == 'POST':
        form = LogEntryForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form without committing to handle the many-to-many relationship
            log_entry = form.save(commit=False)
            log_entry.save()
            # Now save the many-to-many data
            form.save_m2m()
            return redirect('logbook:log_list')
    else:
        form = LogEntryForm()
    return render(request, 'logbook/create_log_entry.html', {'form': form})

@login_required
def log_list(request):
    logs_list = LogEntry.objects.all()
    
    per_page = int(request.GET.get('per_page', 10)) # Get the per_page value or set to default 10
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')  # Get date filters from query parameters
   

    #Filtering logic
    if start_date_filter and end_date_filter:
         try:
             start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
             end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
             logs_list = logs_list.filter(date__range=[start_date,end_date])
         except (ValueError, TypeError):
               pass #Ignore if a bad date value is supplied
    elif start_date_filter:
         try:
             start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
             logs_list = logs_list.filter(date__gte=start_date)
         except (ValueError, TypeError):
               pass
    elif end_date_filter:
         try:
             end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
             logs_list = logs_list.filter(date__lte=end_date)
         except (ValueError, TypeError):
               pass

    logs_list = logs_list.order_by('-logged_at')  # Reverse order
    # Pagination
    paginator = Paginator(logs_list, per_page)
    page = request.GET.get('page', 1)
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    return render(request, 'logbook/log_list.html', {'logs': logs, 'per_page': per_page})

# Edit an existing LogEntry
@login_required
def update_log_entry(request, pk):
    log_entry = get_object_or_404(LogEntry, pk=pk)
    if request.method == "POST":
        form = LogEntryForm(request.POST, request.FILES, instance=log_entry)
        if form.is_valid():
            form.save()
            return redirect('logbook:log_list')
    else:
        form = LogEntryForm(instance=log_entry)
    return render(request, 'logbook/create_log_entry.html', {'form': form})

# Delete a LogEntry
@login_required
def delete_log_entry(request, pk):
    log_entry = get_object_or_404(LogEntry, pk=pk)
    if request.method == "POST":
        log_entry.delete()
        return redirect('logbook:log_list')
    return render(request, 'logbook/log_confirm_delete.html', {'log_entry': log_entry})

@login_required
def log_detail(request, pk):
    log = get_object_or_404(LogEntry, pk=pk)
    return render(request, 'logbook/log_detail.html', {'log': log})
