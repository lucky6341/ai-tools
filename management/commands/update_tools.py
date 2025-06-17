# update_tools.py
from django.core.management.base import BaseCommand
from ai_tools.updater import ToolUpdater

class Command(BaseCommand):
    help = 'Update AI tools information from their websites'
    
    def handle(self, *args, **options):
        updater = ToolUpdater()
        success, total = updater.update_all_tools()
        self.stdout.write(self.style.SUCCESS(f'Updated {success}/{total} tools successfully'))