"""Module for the custom Django rebuild_search_indexes command."""

from django.core import management
from django.db import transaction
from resources.models import Resource
from utils.search_utils import get_search_index_updater


class Command(management.base.BaseCommand):
    """Required command class for the custom Django rebuild_search_indexes command."""

    help = "Rebuild search indexes in database."

    def handle(self, *args, **options):
        """Automatically called when the command is given."""
        for resource in Resource.objects.all():
            transaction.on_commit(get_search_index_updater(resource))
