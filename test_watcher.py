# test_watcher.py
import os
import time
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

# Create a test file in the manuals directory
manuals_path = os.path.join(settings.MEDIA_ROOT, 'manuals')
test_file_path = os.path.join(manuals_path, 'test_file.txt')

print(f"Creating test file at: {test_file_path}")
with open(test_file_path, 'w') as f:
    f.write('This is a test file to trigger the watcher.')

print(f"Test file created. Waiting 5 seconds...")
time.sleep(5)

print(f"Modifying test file...")
with open(test_file_path, 'a') as f:
    f.write('\nThis line was added to test modification events.')

print(f"Test file modified. Waiting 5 seconds...")
time.sleep(5)

print(f"Deleting test file...")
os.remove(test_file_path)

print("Test complete.")