"""Module for the custom Django load_progress_outcomes command."""

import csv
from django.core import management
from learning_area_cards.models import ProgressOutcome

CSV_PATH = 'learning_area_cards/progress-outcomes.csv'


class Command(management.base.BaseCommand):
    """Required command class for the custom Django load_progress_outcomes command."""

    help = "Load progress outcomes to database."

    def handle(self, *args, **options):
        """Automatically called when the load_progress_outcomes command is given."""
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
