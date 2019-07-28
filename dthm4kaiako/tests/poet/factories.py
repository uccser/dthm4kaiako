"""Module for factories for testing the POET application."""

import random
from factory import DjangoModelFactory, Faker, LazyFunction
from factory.django import FileField
from factory import Iterator
from poet.models import (
    Resource,
    ProgressOutcome,
    Submission,
)


class POETFormResourceFactory(DjangoModelFactory):
    """Factory for generating POET form resources."""

    title = Faker('sentence')
    active = True
    pdf = FileField(from_path='tests/poet/example-poet-data.pdf')
    target_progress_outcome = Iterator(ProgressOutcome.objects.all())

    class Meta:
        """Metadata for class."""

        model = Resource


class POETFormSubmissionFactory(DjangoModelFactory):
    """Factory for generating POET form submissions."""

    resource = LazyFunction(
        lambda: random.choice(Resource.objects.all())
    )
    progress_outcome = LazyFunction(
        lambda: random.choice(ProgressOutcome.objects.all())
    )

    class Meta:
        """Metadata for class."""

        model = Submission
