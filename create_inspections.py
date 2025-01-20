import os
import django
from datetime import datetime
from pytz import timezone


# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_ATE.settings')
django.setup()

from daily_inspection.models import DailyInspection
from asset.models import Asset
from daily_inspection.models import DailyInspection, InspectionIdent

# Define timezone
LOCAL_TZ = timezone('Asia/Dubai')  # Replace 'Asia/Dubai' with your +4 timezone if different

now = datetime.now(LOCAL_TZ)
current_hour = now.hour

# Determine shift and time range
if 0 <= current_hour < 14:
    shift = 'DAY'
    time_range = "morning_shift_daily_inspection_required"
else:
    shift = 'NIGHT'
    time_range = "night_shift_daily_inspection_required"

def create_daily_inspections():
    # Filter assets based on the shift conditions
    assets = Asset.objects.filter(**{time_range: True})
    inspections_created = 0

    # Create the InspectionIdent here
    inspection_ident = InspectionIdent.objects.create(shift=shift)
    print(f"Created Inspection ID: {inspection_ident.inspection_ident}")

    for asset in assets:
        # Create a new DailyInspection object with a default
        inspection = DailyInspection.objects.create(
            asset=asset,
            shift=shift,
            inspection_ident=inspection_ident 
        )
        inspections_created += 1

    print(f"{inspections_created} inspection(s) created for the {shift} shift.")
    print(f"Under Inspection ID: {inspection_ident.inspection_ident}, a total of {inspections_created} inspections were created")

if __name__ == "__main__":
    create_daily_inspections()
