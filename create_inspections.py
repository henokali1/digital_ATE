import os
import django
from datetime import datetime
from pytz import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_ATE.settings')
django.setup()

from daily_inspection.models import DailyInspection
from asset.models import Asset

# Define timezone
LOCAL_TZ = timezone('Asia/Dubai')  # Replace 'Asia/Dubai' with your +4 timezone if different

def create_daily_inspections():
    now = datetime.now(LOCAL_TZ)
    current_hour = now.hour

    # Determine shift and time range
    if 0 <= current_hour < 18:
        shift = 'DAY'
        time_range = "morning_shift_daily_inspection_required"
    else:
        shift = 'NIGHT'
        time_range = "night_shift_daily_inspection_required"

    # Filter assets based on the shift conditions
    assets = Asset.objects.filter(**{time_range: True})
    inspections_created = 0

    for asset in assets:
        # Create a new DailyInspection object with a default
        inspection = DailyInspection.objects.create(
            asset=asset,
            shift=shift,
        )
        inspections_created += 1

    print(f"{inspections_created} inspection(s) created for the {shift} shift.")

if __name__ == "__main__":
    create_daily_inspections()
