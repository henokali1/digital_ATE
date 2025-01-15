from django.shortcuts import render, get_object_or_404, redirect
from .models import JobCard
from django.contrib.auth.decorators import login_required
from .forms import JobCardForm

@login_required
def job_card_list(request):
    job_cards = JobCard.objects.all()
    return render(request, 'job_card/job_card_list.html', {'job_cards': job_cards})

@login_required
def job_card_create(request):
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
    if request.method == 'POST':
        job_card.delete()
        return redirect('job_card_list')
    return render(request, 'job_card/job_card_confirm_delete.html', {'job_card': job_card})

@login_required
def job_card_detail(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    return render(request, 'job_card/job_card_detail.html', {'job_card': job_card})
