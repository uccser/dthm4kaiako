"""Module for factories for testing the POET application."""

import random
from factory import (
    DjangoModelFactory,
    Faker,
    LazyFunction,
    post_generation,
)
from factory import Iterator
from poet.models import (
    Resource,
    ProgressOutcome,
    ProgressOutcomeGroup,
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


class POETFormProgressOutcomeGroupFactory(DjangoModelFactory):
    """Factory for generating POET PO groups."""

    name = Faker('sentence')
    active = True

    class Meta:
        """Metadata for class."""

        model = ProgressOutcomeGroup

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add detail to PO group."""
        self.progress_outcomes.add(
            *random.sample(
                list(ProgressOutcome.objects.all()),
                random.randint(3, 8)
            )
        )


def get_progress_outcome():
    """Return a random PO, biased to PO-CT-3."""
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
