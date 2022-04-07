"""Application configuration for resources application."""

from django.apps import AppConfig


class ResourcesAppConfig(AppConfig):
    """Application configuration for resource application."""

    name = 'resources'
    verbose_name = 'Resource Hub'

    def ready(self):
        from resources import signals
