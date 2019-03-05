"""Module for factories for testing the events application."""

import random
from django.contrib.gis.geos import Point
from factory import DjangoModelFactory, Faker, post_generation, LazyFunction, django
from factory.fuzzy import BaseFuzzyAttribute
from factory.faker import faker
from events.models import (
    Sponsor,
    Location,
    Organiser,
)


class SponsorFactory(DjangoModelFactory):
    """Factory for generating event sponsors."""

    name = Faker('company')
    url = Faker('url')

    class Meta:
        """Metadata for class."""

        model = Sponsor


class FuzzyPoint(BaseFuzzyAttribute):
    """Random New Zealand point value."""

    LEFT_LAT = -40.1025
    LEFT_LON = 106.0026
    RIGHT_LAT = -47.1559
    RIGHT_LON = 178.6700

    def fuzz(self):
        lat = random.uniform(self.RIGHT_LAT, self.LEFT_LAT)
        lon = random.uniform(self.LEFT_LON, self.RIGHT_LON)
        return Point(lon, lat)


class LocationFactory(DjangoModelFactory):
    """Factory for generating event sponsors."""

    name = Faker('city')
    description = Faker('paragraph', nb_sentences=5)
    coords = FuzzyPoint()

    class Meta:
        """Metadata for class."""

        model = Location
