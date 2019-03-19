"""Module for the custom Django load_achievement_objectives command."""

import csv
from django.core import management
from authentic_context_cards.models import AchivementObjective

CSV_PATH = 'authentic_context_cards/achievement-objectives.csv'


class Command(management.base.BaseCommand):
    """Required command class for the custom Django load_achievement_objectives command."""

    help = "Load achievement objectives to database."

    def handle(self, *args, **options):
        """Automatically called when the load_achievement_objectives command is given."""

        created_count = 0
        updated_count = 0
        with open(CSV_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obj, created = AchivementObjective.objects.update_or_create(
                    code=row['code'],
                    defaults=row,
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
        print('Achievement objects loaded ({} created, {} updated).'.format(created_count, updated_count))
