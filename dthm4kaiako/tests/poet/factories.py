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
    content = Faker('paragraph', nb_sentences=20)
    target_progress_outcome = Iterator(ProgressOutcome.objects.all())

    class Meta:
        """Metadata for class."""

        model = Resource


def get_progress_outcome():
    progress_outcomes = ProgressOutcome.objects.all()
    if random.randint(1, 5) == 1:
        progress_outcome = progress_outcomes.get(code='PO-CT-3')
    else:
        progress_outcome = random.choice(
            progress_outcomes,
        )
    return progress_outcome


class POETFormSubmissionFactory(DjangoModelFactory):
    """Factory for generating POET form submissions."""

    resource = LazyFunction(
        lambda: random.choice(Resource.objects.all())
    )
    progress_outcome = LazyFunction(get_progress_outcome)

    class Meta:
        """Metadata for class."""

        model = Submission
