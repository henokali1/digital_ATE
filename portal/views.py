from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from job_card.models import JobCard


@login_required
def portal_api(request):
    qs = JobCard.objects.filter(created_by=request.user).order_by('-created_at')
    data = [{'id': jc.pk, 'status': jc.status} for jc in qs]
    return JsonResponse({'requests': data})


@login_required
def portal_home(request):
    if request.method == 'POST':
        task_description = request.POST.get('task_description', '').strip()
        if not task_description:
            messages.error(request, 'Please enter a task description.')
        else:
            JobCard.objects.create(
                task_description=task_description,
                created_by=request.user,
                status='Pending',
                maintenance_type='Corrective',
            )
            messages.success(request, 'Your maintenance request has been submitted successfully.')
            return redirect('portal:home')

    qs = JobCard.objects.filter(created_by=request.user).order_by('-created_at')

    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(job_card_number__icontains=search)

    return render(request, 'portal/portal.html', {
        'my_requests': qs,
        'search': search,
    })
