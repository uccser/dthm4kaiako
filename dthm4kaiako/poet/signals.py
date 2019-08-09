"""Signals for POET application."""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from poet.models import Resource
from utils.update_media_links import update_media_links_in_rich_text


@receiver(pre_save, sender=Resource)
def resource_pre_save(sender, instance, **kwargs):
    """Update resource content with unlocked strings."""
    instance.content = update_media_links_in_rich_text(instance.content)
