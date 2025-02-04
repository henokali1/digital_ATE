from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BugReport
from .forms import BugReportForm

@login_required
def bug_report_list(request):
    bug_reports = BugReport.objects.all()
    return render(request, 'bug_report/bug_report_list.html', {'bug_reports': bug_reports})

@login_required
def bug_report_create(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            bug_report = form.save(commit=False)
            bug_report.reported_by = request.user
            bug_report.save()
            return redirect('bug_report:bug_report_list')
    else:
        form = BugReportForm()
    return render(request, 'bug_report/bug_report_form.html', {'form': form})

@login_required
def bug_report_update(request, pk):
    bug_report = get_object_or_404(BugReport, pk=pk)
    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES, instance=bug_report)
        if form.is_valid():
            form.save()
            return redirect('bug_report:bug_report_list')
    else:
        form = BugReportForm(instance=bug_report)
    return render(request, 'bug_report/bug_report_form.html', {'form': form})

@login_required
def bug_report_delete(request, pk):
    bug_report = get_object_or_404(BugReport, pk=pk)
    if request.method == 'POST':
        bug_report.delete()
        return redirect('bug_report:bug_report_list')
    return render(request, 'bug_report/bug_report_confirm_delete.html', {'bug_report': bug_report})

@login_required
def bug_report_detail(request, pk):
    bug_report = get_object_or_404(BugReport, pk=pk)
    return render(request, 'bug_report/bug_report_detail.html', {'bug_report': bug_report})