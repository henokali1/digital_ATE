from django.shortcuts import render, get_object_or_404, redirect
from .models import JobCard
from django.contrib.auth.decorators import login_required
from .forms import JobCardForm, CSVImportForm
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from datetime import timedelta, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User
from django import forms
from logbook.models import LogEntry
from .models import JobCard, JobCardMessage, JobCardImage
from .forms import JobCardMessageForm
import csv
import io
from django.contrib import messages
from location.models import Location

@login_required
def job_card_chat(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    messages = job_card.messages.all().prefetch_related('images')
    
    if request.method == 'POST':
        print("Files in request:", request.FILES)
        form = JobCardMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.job_card = job_card
            message.user = request.user
            message.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images[]')
            for image in images:
                JobCardImage.objects.create(message=message, image=image)
            
            print(f"Saved {len(images)} images for message {message.id}")
                
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': message.message,
                    'user': message.user.get_full_name() or message.user.username,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'images': [{'url': img.image.url} for img in message.images.all()]
                })
            return redirect('job_card_detail', pk=pk)
    else:
        form = JobCardMessageForm()
    
    return render(request, 'job_card/job_card_chat.html', {
        'job_card': job_card,
        'messages': messages,
        'form': form
    })


@login_required
def job_card_list(request):
    filter = request.GET.get('filter', 'all')
    per_page = int(request.GET.get('per_page', 25))  # Get the per_page value or set to default 25

    # Get filter values from query parameters
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    maintenance_type_filter = request.GET.get('maintenance_type')
    acknowledged_filter = request.GET.get('acknowledged')
    assigned_to_filter = request.GET.get('assigned_to')
    
    today = date.today() #Get current date

    if filter == 'assigned':
        job_cards_list = JobCard.objects.filter(assigned_users=request.user)
    elif filter == 'overdue':
       job_cards_list = JobCard.objects.filter(due_date__lt=today).exclude(status='Completed')
    elif filter == 'upcoming':
         job_cards_list = JobCard.objects.filter(
              start_date__gt=today # start date should be in the future
        )
    else:
        job_cards_list = JobCard.objects.all()

    # Apply filters to the queryset
    if status_filter:
        job_cards_list = job_cards_list.filter(status=status_filter)
    if priority_filter:
        job_cards_list = job_cards_list.filter(priority_level=priority_filter)
    if maintenance_type_filter:
        job_cards_list = job_cards_list.filter(maintenance_type=maintenance_type_filter)
    if acknowledged_filter:
            if acknowledged_filter == 'True':
                job_cards_list = job_cards_list.filter(acknowledged=True)
            elif acknowledged_filter == 'False':
                job_cards_list = job_cards_list.filter(acknowledged=False)
    if assigned_to_filter:
          job_cards_list = job_cards_list.filter(assigned_users__id=assigned_to_filter)

    #Filter for date range if there is a start date and due date
    if filter != 'overdue' and filter != 'upcoming': # Do this filter only when overdue and upcoming filter is not used
        job_cards_list = job_cards_list.filter(
            Q(start_date__isnull=True) | Q(start_date__lte=today),
            Q(due_date__isnull=True) | Q(due_date__gte=today)
        )
    
    job_cards_list = job_cards_list.order_by('-created_at') # Order by newest first

     # Pagination
    paginator = Paginator(job_cards_list, per_page)
    page = request.GET.get('page', 1)
    try:
        job_cards = paginator.page(page)
    except PageNotAnInteger:
        job_cards = paginator.page(1)
    except EmptyPage:
        job_cards = paginator.page(paginator.num_pages)

    users = User.objects.all() #Get all users
    return render(request, 'job_card/job_card_list.html', {'job_cards': job_cards, 'filter': filter, 'per_page': per_page, 'users':users, 'job_card': JobCard})

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
            return render(request, 'job_card/job_card_form.html', {'form': form})
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
            return render(request, 'job_card/job_card_form.html', {'form': form})
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

        if new_status == 'Completed':
            if job_card.maintenance_type == 'Preventive' and not job_card.preventive_maintenance_id:
                return render(request, 'job_card/job_card_detail.html', {'job_card': job_card, 'error': 'A preventive maintenance record must be created before marking the job card as completed.'})

            if job_card.maintenance_type == 'Corrective' and not job_card.corrective_maintenance_id:
                return render(request, 'job_card/job_card_detail.html', {'job_card': job_card, 'error': 'A corrective maintenance record must be created before marking the job card as completed.'})
        
        # Setting the status
        job_card.status = new_status
        if new_status == 'Completed':
             job_card.completed_at = timezone.now() # Set completed_at
             job_card.time_to_complete = job_card.completed_at - job_card.created_at # calculate duration
        
        job_card.save() 
        return redirect('job_card_detail', pk=pk)
    
    return redirect('job_card_detail', pk=pk)

@login_required
def job_card_add_remark_to_logbook(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)

    if request.method == 'POST' and job_card.remarks:
           current_time = timezone.localtime()
           log_entry = LogEntry.objects.create(
                date = current_time.date(),
                time = current_time.time(),
                location = job_card.location,
                remarks = f"[Job Card: {job_card.job_card_number}] : {job_card.remarks}",
                )
           log_entry.initials.set(job_card.assigned_users.all())
           return redirect('job_card_detail', pk=pk)
    return redirect('job_card_detail', pk=pk)

@login_required
def import_job_cards(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to import job cards.")
    if request.method == 'POST':
      
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                 messages.error(request, 'Please upload a CSV file.')
                 return redirect('import_job_cards')
            # Read CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(decoded_file))
                
                success_count = 0
                error_count = 0
                errors = []
                for row in csv_data:
                    try:
                        location = Location.objects.get(name=row['location'])
                    
                         # Get the User objects for assigned users based on usernames in CSV
                        assigned_users = []
                        assigned_usernames = row.get('assigned_users', '').split(',')
                        for username in assigned_usernames:
                             try:
                                 user = User.objects.get(username=username.strip())
                                 assigned_users.append(user)
                             except User.DoesNotExist:
                                    errors.append(f"User '{username.strip()}' does not exist.")
                                    continue
                         # Create job card
                     
                        job_card = JobCard.objects.create(
                            task_description=row['task_description'],
                            priority_level=row.get('priority_level', ''),
                            maintenance_type=row.get('maintenance_type', 'Not Required'),
                            location=location,
                            status=row['status'],
                            created_by=request.user,
                            start_date=row.get('start_date', None),
                            due_date=row.get('due_date', None),
                            remarks=row.get('remarks',''),
                           )
                        job_card.assigned_users.set(assigned_users)
                        success_count += 1
                    except Exception as e:
                       error_count += 1
                       errors.append(f"Row {csv_data.line_num}: {str(e)}")
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} job cards.')
                if error_count > 0:
                    messages.warning(request, f'Failed to import {error_count} job cards.')
                    for error in errors:
                       messages.error(request, error)

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                return redirect('import_job_cards')

            return redirect('job_card_list')
    else:
        form = CSVImportForm()
    return render(request, 'job_card/import_job_cards.html', {'form': form})

@login_required
def download_sample_csv(request):
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_job_cards.csv"'

    # Create CSV writer
    writer = csv.writer(response)
    
    # Write headers
    writer.writerow([
        'task_description', 'priority_level', 'maintenance_type', 'location', 
        'status', 'assigned_users','start_date', 'due_date','remarks'
    ])
    
    # Write sample data
    writer.writerow([
        'Sample Task Description 1', 'Medium', 'Corrective', 'Tower',
        'Pending', 'cns.ce,user1', '2024-02-10', '2024-03-10', 'Sample remarks'
    ])
    writer.writerow([
        'Sample Task Description 2', 'High', 'Preventive', 'Ground',
        'In Progress', 'cns.ce,user2', '2024-03-10', '2024-04-10','Another Sample remarks'
    ])

    return response
