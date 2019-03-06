"""Module for factories for testing the events application."""

import random
import pytz
from datetime import timedelta
from django.contrib.gis.geos import Point
from tests.utils import random_boolean
from factory import DjangoModelFactory, Faker, post_generation, LazyFunction, LazyAttribute
from factory.fuzzy import BaseFuzzyAttribute
from factory.faker import faker
from events.models import (
    Sponsor,
    Organiser,
    Series,
    Event,
    Location,
)


class SponsorFactory(DjangoModelFactory):
    """Factory for generating event sponsors."""

    name = Faker('company')
    url = Faker('url')

    class Meta:
        """Metadata for class."""

        model = Sponsor


class OrganiserFactory(DjangoModelFactory):
    """Factory for generating event organisers."""

    name = Faker('company')
    url = Faker('url')

    class Meta:
        """Metadata for class."""

        model = Organiser


class SeriesFactory(DjangoModelFactory):
    """Factory for generating event series."""

    name = Faker('words', nb=2)
    abbreviation = Faker('company_suffix')

    class Meta:
        """Metadata for class."""

        model = Series


class EventFactory(DjangoModelFactory):
    """Factory for generating events."""

    name = Faker('sentence', nb_words=3)
    description = Faker('paragraph', nb_sentences=50)
    registration_link = Faker('url')
    published = True
    start = Faker('date_time_between', start_date='-1y', end_date='+3y', tzinfo=pytz.timezone('Pacific/Auckland'))
    end = LazyAttribute(lambda obj: obj.start + timedelta(days=random.randint(0, 3)))
    accessible_online = LazyFunction(random_boolean)

    class Meta:
        """Metadata for class."""

        model = Event

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add detail to event."""
        FAKER = faker.Faker()

        # Set location
        # 80% chance one location, otherwise multiple
        if random.randint(1, 5) == 1:
            self.locations.add(*random.sample(
                list(Location.objects.all()),
                random.randint(2, 4)
            ))
        else:
            self.locations.add(random.choice(Location.objects.all()))

        # Set organiser
        # 80% chance one organiser, otherwise multiple
        if random.randint(1, 5) == 1:
            self.organisers.add(*random.sample(
                list(Organiser.objects.all()),
                random.randint(2, 3)
            ))
        else:
            self.organisers.add(random.choice(Organiser.objects.all()))

        # Set sponsor
        # 80% chance one sponsor, otherwise multiple
        if random.randint(1, 5) == 1:
            self.sponsors.add(*random.sample(
                list(Sponsor.objects.all()),
                random.randint(2, 4)
            ))
        else:
            self.sponsors.add(random.choice(Sponsor.objects.all()))

        # Set series
        # 50% chance of being in a series
        if random.randint(1, 2) == 1:
            self.series = random.choice(Series.objects.all())
