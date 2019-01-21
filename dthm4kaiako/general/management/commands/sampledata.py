"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from tests.dtta.factories import NewsArticleFactory

class Command(management.base.BaseCommand):
    """Required command class for the custom Django sampledata command."""

    help = "Add sample data to database."

    def handle(self, *args, **options):
        """Automatically called when the sampledata command is given."""

        # Only run in debug mode
        if not settings.DEBUG:
            raise management.base.CommandError(
                'This command can only be executed in DEBUG mode.'
            )

        # Clear all data
        management.call_command('flush', interactive=False)

        # Create admin account
        User = get_user_model()
        User.objects.filter(email='admin@example.com').delete()
        User.objects.create_superuser('admin', 'admin@example.com', 'password')

        # DTTA
        # News Articles
        NewsArticleFactory.create_batch(size=100)
