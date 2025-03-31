import os
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from om_manuals.models import Manual
from django.contrib.auth.decorators import login_required

def get_folder_structure(base_dir):
    """
    Generates a nested dictionary representing the folder structure
    of the manuals directory.
    """
    structure = {}
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            structure[item] = {'type': 'folder', 'name': item}  # Mark as folder
        else:
            structure[item] = {'type': 'file', 'name': item}  # Mark as file
    return structure

@login_required
def manual_list(request):
    query = request.GET.get('q')
    path = request.GET.get('path', 'manuals')  # Get the path from the query parameters. Default to 'manuals'
    manuals = []

    if query:
        manuals = Manual.objects.filter(
            Q(title__icontains=query) |
            Q(section__icontains=query) |
            Q(folder__icontains=query)
        ).order_by('section', 'folder', 'title')

    #Change the default value, since we removed the manuals directory, use MEDIA_ROOT
    manuals_path = os.path.join(settings.MEDIA_ROOT, path) #append folder name

    folder_structure = get_folder_structure(manuals_path)

    return render(request, 'om_manuals/manual_list.html', {
        'manuals': manuals,
        'query': query,
        'folder_structure': folder_structure,
        'current_path': path,  # Pass the current path to the template
    })