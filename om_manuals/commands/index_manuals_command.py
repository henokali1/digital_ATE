# om_manuals/management/commands/index_manuals_command.py
from django.core.management.base import BaseCommand
from om_manuals.utils import index_manuals, remove_deleted_manuals

class Command(BaseCommand):
    help = 'Indexes the manuals in the media directory'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting manual indexing...'))
        index_manuals()
        remove_deleted_manuals()
        self.stdout.write(self.style.SUCCESS('Manual indexing completed.'))