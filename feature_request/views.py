from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FeatureRequest
from .forms import FeatureRequestForm


@login_required
def feature_request_list(request):
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'all':
        feature_requests = FeatureRequest.objects.all()
    else:
        feature_requests = FeatureRequest.objects.filter(status=status_filter)

    return render(request, 'feature_request/feature_request_list.html', {'feature_requests': feature_requests, 'FeatureRequest':FeatureRequest})

@login_required
def feature_request_create(request):
    if request.method == 'POST':
        form = FeatureRequestForm(request.POST, request.FILES)
        if form.is_valid():
            feature_request = form.save(commit=False)
            feature_request.requested_by = request.user
            feature_request.save()
            return redirect('feature_request:feature_request_list')
    else:
        form = FeatureRequestForm()
    return render(request, 'feature_request/feature_request_form.html', {'form': form})

@login_required
def feature_request_update(request, pk):
    feature_request = get_object_or_404(FeatureRequest, pk=pk)
    if request.method == 'POST':
        form = FeatureRequestForm(request.POST, request.FILES, instance=feature_request)
        if form.is_valid():
            form.save()
            return redirect('feature_request:feature_request_list')
    else:
        form = FeatureRequestForm(instance=feature_request)
    return render(request, 'feature_request/feature_request_form.html', {'form': form})

@login_required
def feature_request_delete(request, pk):
    feature_request = get_object_or_404(FeatureRequest, pk=pk)
    if request.method == 'POST':
        feature_request.delete()
        return redirect('feature_request:feature_request_list')
    return render(request, 'feature_request/feature_request_confirm_delete.html', {'feature_request': feature_request})

@login_required
def feature_request_detail(request, pk):
    feature_request = get_object_or_404(FeatureRequest, pk=pk)

    if request.method == 'POST' and request.user.is_superuser:
        new_status = request.POST.get('status')
        comments = request.POST.get('comments')
        feature_request.status = new_status
        feature_request.comments = comments
        feature_request.save()
        return redirect('feature_request:feature_request_detail', pk=pk)  # Refresh the page

    return render(request, 'feature_request/feature_request_detail.html', {'feature_request': feature_request})
