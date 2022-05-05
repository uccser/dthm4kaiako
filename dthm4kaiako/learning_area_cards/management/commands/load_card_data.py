"""Module for the custom Django load_card_data command."""

from django.core import management


class Command(management.base.BaseCommand):
    """Required command class for the custom Django load_card_data command."""

    help = "Update all data for the learning area cards application."

    def handle(self, *args, **options):
        """Automatically called when the load_card_data command is given."""
        management.call_command("load_achievement_objectives")
        management.call_command("load_progress_outcomes")
