"""Base test class with methods implemented for Django testing."""

from django.test import TestCase
from tests.events.EventDataGenerator import EventDataGenerator


class BaseTest(TestCase):
    """Base test class for Django testing."""

    def __init__(self, *args, **kwargs):
        """Create a BaseTest object."""
        super().__init__(*args, **kwargs)
        self.event_data = EventDataGenerator()
