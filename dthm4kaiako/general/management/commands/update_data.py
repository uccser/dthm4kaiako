"""Module for the custom Django update_data command."""

from django.core import management
from django.conf import settings


class Command(management.base.BaseCommand):
    """Required command class for the custom Django update_data command."""

    help = "Update data in database."

    def handle(self, *args, **options):
        """Automatically called when the sampledata command is given."""

        # Only run in staging environment or local development
        if settings.STAGING_ENVIRONMENT or settings.DEBUG:
            management.call_command('sampledata')
            print('Sample data added.\n')

        management.call_command('load_card_data')
        print('Learning area card data loaded.\n')

        management.call_command('load_poet_data')
        print('POET data loaded.\n')
