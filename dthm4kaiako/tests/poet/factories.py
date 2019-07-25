"""Module for factories for testing the resources application."""

import random
from factory import DjangoModelFactory, Faker, post_generation, LazyFunction
from factory.django import FileField
from factory import Iterator
from poet.models import (
    Resource,
    ProgressOutcome,
)

CONTENT_PRIMARY = 1
CONTENT_SECONDARY = 2
CONTENT_BOTH = 3


class ResourceFactory(DjangoModelFactory):
    """Factory for generating resources."""

    title = Faker('sentence')
    active = True
    pdf = FileField(from_path='tests/poet/example-poet-data.pdf')
    target_progress_outcome = Iterator(ProgressOutcome.objects.all())

    class Meta:
        """Metadata for class."""

        model = Resource
