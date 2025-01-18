# daily_inspection/management/commands/create_daily_inspections.py
import os
import sys
import django
from pathlib import Path

def setup_django():
    current_path = Path(__file__).resolve()
    project_root = current_path.parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_ATE.settings')
    try:
        django.setup()
    except Exception as e:
        print(f"Failed to setup Django: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_django()

try:
    from django.core.management.base import BaseCommand
    from django.utils import timezone
    from django.contrib.auth import get_user_model
    from asset.models import Asset
    from daily_inspection.models import DailyInspection
    
    User = get_user_model()
except Exception as e:
    print(f"Failed to import required modules: {e}")
    sys.exit(1)

class Command(BaseCommand):
    help = 'Creates daily inspections for assets based on shift requirements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-shift',
            choices=['Day', 'Night'],
            help='Force create inspections for a specific shift (for testing)',
        )

    def handle(self, *args, **kwargs):
        current_time = timezone.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        self.stdout.write(f"Current time: {current_time}")
        
        try:
            system_user = User.objects.get(username='system')
            self.stdout.write(f"Found system user: {system_user}")
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('System user not found. Please create a user with username "system"'))
            return

        force_shift = kwargs.get('force_shift')
        if force_shift:
            self.stdout.write(f"Forcing creation of {force_shift} shift inspections")
            if force_shift == 'Day':
                assets = Asset.objects.filter(morning_shift_daily_inspection_required=True)
            else:  # Night shift
                assets = Asset.objects.filter(night_shift_daily_inspection_required=True)
            shift = force_shift
        else:
            self.stdout.write(f"Checking time-based conditions: Hour={current_hour}, Minute={current_minute}")
            if current_hour == 0 and current_minute == 0:  # 00:00
                self.stdout.write("Condition met: Creating day shift inspections")
                assets = Asset.objects.filter(morning_shift_daily_inspection_required=True)
                shift = 'Day'
            elif current_hour == 14:
                if current_minute == 0:
                    self.stdout.write("Condition met: Creating night shift inspections (14:00)")
                    assets = Asset.objects.filter(night_shift_daily_inspection_required=True)
                    shift = 'Night'
                elif current_minute == 25:
                    self.stdout.write("Condition met: Creating additional night shift inspections (14:25)")
                    assets = Asset.objects.filter(night_shift_daily_inspection_required=True)
                    shift = 'Night'
                else:
                    self.stdout.write("No time condition met for 14:xx")
                    return
            else:
                self.stdout.write("No time conditions met")
                return

        # Debug output for assets
        asset_count = assets.count()
        self.stdout.write(f"Found {asset_count} assets requiring inspection")
        
        if asset_count == 0:
            self.stdout.write(self.style.WARNING(f"No assets found requiring {shift} shift inspection"))
            self.stdout.write("Checking asset requirements:")
            all_assets = Asset.objects.all()
            self.stdout.write(f"Total assets in database: {all_assets.count()}")
            for asset in all_assets:
                self.stdout.write(f"Asset: {asset.name}")
                self.stdout.write(f"  Morning inspection required: {asset.morning_shift_daily_inspection_required}")
                self.stdout.write(f"  Night inspection required: {asset.night_shift_daily_inspection_required}")
            return

        created_count = 0
        for asset in assets:
            try:
                self.stdout.write(f"Creating inspection for asset: {asset.name}")
                DailyInspection.objects.create(
                    asset=asset,
                    inspected_by=system_user,
                    shift=shift,
                    status='Off'
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create inspection for asset {asset.name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {shift} shift inspections for {created_count} assets'
            )
        )

if __name__ == "__main__":
    command = Command()
    command.handle(force_shift='Day')  # Force day shift when running directly