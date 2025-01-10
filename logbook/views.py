# logbook/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LogEntryForm
from .models import Location, LogEntry
from django.contrib.auth.models import User

def create_log_entry(request):
    if request.method == 'POST':
        form = LogEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('logbook:log_list')
    else:
        form = LogEntryForm()
    return render(request, 'logbook/create_log_entry.html', {'form': form})

def log_list(request):
    logs = LogEntry.objects.all()
    return render(request, 'logbook/log_list.html', {'logs': logs})

# Edit an existing LogEntry
def update_log_entry(request, pk):
    log_entry = get_object_or_404(LogEntry, pk=pk)
    if request.method == "POST":
        form = LogEntryForm(request.POST, request.FILES, instance=log_entry)
        if form.is_valid():
            form.save()
            return redirect('logbook:log_list')
    else:
        form = LogEntryForm(instance=log_entry)
    return render(request, 'logbook/log_form.html', {'form': form})

# Delete a LogEntry
def delete_log_entry(request, pk):
    log_entry = get_object_or_404(LogEntry, pk=pk)
    if request.method == "POST":
        log_entry.delete()
        return redirect('logbook:log_list')
    return render(request, 'logbook/log_confirm_delete.html', {'log_entry': log_entry})