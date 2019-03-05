"""Module for factories for testing the events application."""

import random
from django.contrib.gis.geos import Point
from factory import DjangoModelFactory, Faker, post_generation, LazyFunction, django
from factory.fuzzy import BaseFuzzyAttribute
from factory.faker import faker
from events.models import (
    Sponsor,
    Organiser,
)


class SponsorFactory(DjangoModelFactory):
    """Factory for generating event sponsors."""

    name = Faker('company')
    url = Faker('url')

    class Meta:
        """Metadata for class."""

        model = Sponsor
