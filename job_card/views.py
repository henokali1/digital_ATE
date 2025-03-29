from django.shortcuts import render, get_object_or_404, redirect
from .models import JobCard
from django.contrib.auth.decorators import login_required
from .forms import JobCardForm, CSVImportForm
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from datetime import timedelta, date, datetime
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
    search_term = request.GET.get('search', '')  # Get the search term from the request

    # Get filter values from query parameters
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    maintenance_type_filter = request.GET.get('maintenance_type')
    acknowledged_filter = request.GET.get('acknowledged')
    assigned_to_filter = request.GET.get('assigned_to')

    # Date Range Filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    date_range = request.GET.get('date_range')

    today = date.today()  # Get current date
    current_date = datetime.now().date()

    if filter == 'assigned':
        job_cards_list = JobCard.objects.filter(assigned_users=request.user)
    elif filter == 'overdue':
        job_cards_list = JobCard.objects.filter(due_date__lt=today).exclude(status='Completed')
    elif filter == 'upcoming':
        job_cards_list = JobCard.objects.filter(
            start_date__gt=today  # start date should be in the future
        )
    else:
        # exclude the job cards whose start date is greater than today
        job_cards_list = JobCard.objects.exclude(start_date__gt=today)

    # Apply date range filters
    if start_date and end_date:
        job_cards_list = job_cards_list.filter(created_at__date__range=[start_date, end_date])
    elif date_range:
        if date_range == 'this_week':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            job_cards_list = job_cards_list.filter(created_at__date__range=[start_week, end_week])
        elif date_range == 'this_month':
            start_month = date(today.year, today.month, 1)
            end_month = date(today.year, today.month, 1) + timedelta(days=32)
            end_month = end_month.replace(day=1) - timedelta(days=1)
            job_cards_list = job_cards_list.filter(created_at__date__range=[start_month, end_month])
        elif date_range == 'this_year':
            start_year = date(today.year, 1, 1)
            end_year = date(today.year, 12, 31)
            job_cards_list = job_cards_list.filter(created_at__date__range=[start_year, end_year])

    # Apply other filters to the queryset
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

    # Apply the search filter
    if search_term:
        job_cards_list = job_cards_list.filter(
            Q(job_card_number__icontains=search_term) |
            Q(task_description__icontains=search_term) |
            Q(location__name__icontains=search_term) |  # Assuming location has a 'name' field
            Q(remarks__icontains=search_term)
        )

    # Calculate counts before pagination
    total_count = job_cards_list.count()
    completed_count = job_cards_list.filter(status='Completed').count()
    pending_count = job_cards_list.filter(status='Pending').count()
    in_progress_count = job_cards_list.filter(status='In Progress').count()
    overdue_count = JobCard.objects.filter(due_date__lt=today).exclude(status='Completed').count()

    job_cards_list = job_cards_list.order_by('-created_at')  # Order by newest first

    # Pagination
    paginator = Paginator(job_cards_list, per_page)
    page = request.GET.get('page', 1)
    try:
        job_cards = paginator.page(page)
    except PageNotAnInteger:
        job_cards = paginator.page(1)
    except EmptyPage:
        job_cards = paginator.page(paginator.num_pages)

    users = User.objects.all()  # Get all users
    return render(request, 'job_card/job_card_list.html', {
        'job_cards': job_cards,
        'filter': filter,
        'per_page': per_page,
        'users': users,
        'job_card': JobCard,
        'today': current_date,
        'search_term': search_term,  # Pass the search term to the template

        # Dashboard counts
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'overdue_count': overdue_count,
    })


@login_required
def job_card_create(request):
    user_can_create = False
    if request.user.is_superuser:
        user_can_create = True
    else:
        # Check if user has a profile and a position with the permission flag set
        try:
            # Access profile via the related name 'userprofile' (lowercase)
            profile = request.user.userprofile
            if profile.position and profile.position.can_create_job_cards:
                user_can_create = True
        except User.userprofile.RelatedObjectDoesNotExist:
            pass
        except AttributeError:
             pass


    if not user_can_create:
        return HttpResponseForbidden("You are not authorized to create job cards.")


    if request.method == 'POST':
        form = JobCardForm(request.POST, request.FILES)
        if form.is_valid():
            job_card = form.save(commit=False)
            job_card.created_by = request.user
            job_card.save()
            form.save_m2m()  # Save many-to-many relationships (like assigned_users)
            messages.success(request, f'Job Card {job_card.job_card_number} created successfully.') # Optional success message
            return redirect('job_card_list')
        else:
            # Pass form with errors back to template
            messages.error(request, 'Please correct the errors below.') # Optional error message
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
        form = JobCardForm(request.POST, request.FILES, instance=job_card)
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
        # Handle the image upload
        if 'status_update_image' in request.FILES:
            job_card.status_update_image = request.FILES['status_update_image']
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
                        start_date_str = row.get('start_date')
                        due_date_str = row.get('due_date')
                        
                        start_date = None
                        due_date = None

                        if start_date_str:
                            try:
                                start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
                            except ValueError:
                                errors.append(f"Invalid start date format: {start_date_str}. Use MM/DD/YYYY.")
                                start_date = None  # Ensure start_date is None if parsing fails

                        if due_date_str:
                            try:
                                due_date = datetime.strptime(due_date_str, '%m/%d/%Y').date()
                            except ValueError:
                                errors.append(f"Invalid due date format: {due_date_str}. Use MM/DD/YYYY.")
                                due_date = None  # Ensure due_date is None if parsing fails
                       
                        requires_oem_support = row.get('requires_oem_support', 'False').lower() == 'true'
                        job_card = JobCard.objects.create(
                            task_description=row['task_description'],
                            priority_level=row.get('priority_level', ''),
                            maintenance_type=row.get('maintenance_type', 'Not Required'),
                            location=location,
                            status=row['status'],
                            created_by=request.user,
                            start_date=start_date,
                            due_date=due_date,
                            remarks=row.get('remarks',''),
                            requires_oem_support=requires_oem_support,
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
                messages.add_message(request, messages.INFO, "Custom message", extra_tags="my_custom_tag")
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
        'status', 'assigned_users','start_date', 'due_date','remarks', 'requires_oem_support'
    ])
    
    # Write sample data (MM/DD/YYYY format)
    writer.writerow([
        'Sample Task Description 1', 'Medium', 'Corrective', 'VCR',
        'Pending', 'cns.ce@fans.ae,cns.104@fans.ae', '02/10/2025', '03/10/2025', 'Sample remarks', 'True'
    ])
    writer.writerow([
        'Sample Task Description 2', 'High', 'Preventive', 'ACR',
        'In Progress', 'cns.ce@fans.ae,cns.104@fans.ae', '03/10/2025', '04/10/2025','Another Sample remarks', 'False'
    ])

    return response