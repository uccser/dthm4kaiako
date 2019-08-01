"""Module for the custom Django load_poet_data command."""

import csv
from django.core import management
from poet.models import ProgressOutcome

CSV_PATH = 'poet/content/progress-outcomes.csv'


class Command(management.base.BaseCommand):
    """Required command class for the custom Django load_poet_data command."""

    help = "Load POET data to database."

    def handle(self, *args, **options):
        """Automatically called when the load_poet_data command is given."""
        created_count = 0
        updated_count = 0
        with open(CSV_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obj, created = ProgressOutcome.objects.update_or_create(
                    code=row['code'],
                    defaults=row,
                )
                if created:
                    created_count += 1
                    print('Created {}'.format(obj.code))
                else:
                    updated_count += 1
                    print('Updated {}'.format(obj.code))
        print('Progress outcomes loaded ({} created, {} updated).'.format(created_count, updated_count))
