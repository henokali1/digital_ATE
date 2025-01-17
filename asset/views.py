from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset
from .forms import AssetForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return HttpResponse("Welcome to Digital ATE!")

# List all assets
@login_required
def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'asset/asset_list.html', {'assets': assets, 'user': request.user})

# Create a new asset
@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('asset_list')  # Redirect to the list page after saving
    else:
        form = AssetForm()
    return render(request, 'asset/asset_form.html', {'form': form})

@login_required
def asset_detail(request, id):
    asset = get_object_or_404(Asset, id=id)
    return render(request, 'asset/asset_detail.html', {'asset': asset})

# Update an existing asset
@login_required
def asset_edit(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'asset/asset_form.html', {'form': form})

@login_required
def asset_delete(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')
    return render(request, 'asset/asset_confirm_delete.html', {'asset': asset})
