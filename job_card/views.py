from django.shortcuts import render, get_object_or_404, redirect
from .models import JobCard
from django.contrib.auth.decorators import login_required
from .forms import JobCardForm
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def job_card_list(request):
    filter = request.GET.get('filter', 'all')
    per_page = int(request.GET.get('per_page', 10)) # Get the per_page value or set to default 10
    if filter == 'assigned':
       job_cards_list = JobCard.objects.filter(assigned_users=request.user).order_by('-created_at') # Order by newest first
    else:
        job_cards_list = JobCard.objects.all().order_by('-created_at') # Order by newest first

     # Pagination
    paginator = Paginator(job_cards_list, per_page)
    page = request.GET.get('page', 1)
    try:
        job_cards = paginator.page(page)
    except PageNotAnInteger:
        job_cards = paginator.page(1)
    except EmptyPage:
        job_cards = paginator.page(paginator.num_pages)
    return render(request, 'job_card/job_card_list.html', {'job_cards': job_cards, 'filter': filter, 'per_page': per_page})

@login_required
def job_card_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to create job cards.")
    if request.method == 'POST':
        form = JobCardForm(request.POST)
        if form.is_valid():
            job_card = form.save(commit=False)
            job_card.created_by = request.user
            job_card.save()
            form.save_m2m()
            return redirect('job_card_list')
    else:
        form = JobCardForm()
    return render(request, 'job_card/job_card_form.html', {'form': form})

@login_required
def job_card_update(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to edit job cards.")
    if request.method == 'POST':
        form = JobCardForm(request.POST, instance=job_card)
        if form.is_valid():
            form.save()
            return redirect('job_card_list')
    else:
        form = JobCardForm(instance=job_card)
    return render(request, 'job_card/job_card_form.html', {'form': form})

@login_required
def job_card_delete(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    if not request.user.is_superuser:
         return HttpResponseForbidden("You are not authorized to delete job cards.")
    if request.method == 'POST':
        job_card.delete()
        return redirect('job_card_list')
    return render(request, 'job_card/job_card_confirm_delete.html', {'job_card': job_card})

@login_required
def job_card_detail(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    return render(request, 'job_card/job_card_detail.html', {'job_card': job_card})

@login_required
def job_card_acknowledge(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)

    if request.user not in job_card.assigned_users.all():
       return HttpResponseForbidden("You are not authorized to acknowledge this job card.")

    if request.method == 'POST':
        job_card.acknowledged = True
        job_card.acknowledged_at = timezone.now()
        job_card.time_to_acknowledge = job_card.acknowledged_at - job_card.created_at
        job_card.save(update_fields=['acknowledged','acknowledged_at', 'time_to_acknowledge']) # modified here
        return redirect('job_card_detail', pk=pk)
    
    return render(request, 'job_card/job_card_acknowledge.html', {'job_card': job_card})

@login_required
def job_card_update_status(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)

    if request.user not in job_card.assigned_users.all():
       return HttpResponseForbidden("You are not authorized to change the status of this job card.")

    if request.method == 'POST':
         new_status = request.POST.get('status')
         job_card.remarks = request.POST.get('remarks')

         if new_status == 'Completed': #Check if the status is completed
             job_card.completed_at = timezone.now() # Set completed_at
             job_card.time_to_complete = job_card.completed_at - job_card.created_at # calculate duration
             job_card.save(update_fields=['status', 'remarks','completed_at','time_to_complete'])
         else:
            job_card.save(update_fields=['status', 'remarks']) #save when status is not completed
         return redirect('job_card_detail', pk=pk)
    
    return redirect('job_card_detail', pk=pk)