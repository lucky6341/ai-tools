# import_tools.py
from django.core.management.base import BaseCommand
from ai_tools.models import AITool, Category
import csv

class Command(BaseCommand):
    help = 'Import AI tools from CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)
    
    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Process each row and create tools
                # ...