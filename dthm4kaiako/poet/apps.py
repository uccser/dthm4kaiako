"""Application configuration for POET application."""

from django.apps import AppConfig


class POETAppConfig(AppConfig):
    """Application configuration for POET application."""

    name = 'poet'

    def ready(self):
        """Run when application is ready."""
        import poet.signals  # noqa
