"""Module for factories for tesing resources application."""

from factory import DjangoModelFactory, Faker
from resources.models import (
    Resource,
    ResourceComponent,
)
import pytz


class ResourceFactory(DjangoModelFactory):
    """Factory for generating resources."""

    name = Faker('sentence')
    description = Faker('paragraph', nb_sentences=5)

    class Meta:
        """Metadata for class."""

        model = Resource
