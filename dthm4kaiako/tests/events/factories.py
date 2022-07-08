"""Module for factories for testing the events application."""

import random
import pytz
from datetime import timedelta
from tests.test_utils import random_boolean
from factory import Faker, post_generation, LazyFunction, LazyAttribute
from factory.django import DjangoModelFactory
from factory.faker import faker
from users.models import Entity
from events.models import (
    Series,
    Event,
    Location,
    Session,
)


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
    # registration_link = Faker('url') #TODO: turn off while testing register button 
    published = True
    show_schedule = True
    start = Faker('date_time_between', start_date='-1y', end_date='+3y', tzinfo=pytz.timezone('Pacific/Auckland'))
    end = LazyAttribute(lambda obj: obj.start)
    accessible_online = LazyFunction(random_boolean)

    class Meta:
        """Metadata for class."""

        model = Event

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add detail to event."""
        # Set featured
        # 20% chance
        if random.randint(1, 5) == 1:
            self.featured = True

        # Set show schedule
        # 10% chance to hide
        if random.randint(1, 10) == 1:
            self.show_schedule = False

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
                list(Entity.objects.all()),
                random.randint(2, 3)
            ))
        else:
            self.organisers.add(random.choice(Entity.objects.all()))

        # Set sponsor
        # 80% chance one sponsor, otherwise multiple
        if random.randint(1, 5) == 1:
            self.sponsors.add(*random.sample(
                list(Entity.objects.all()),
                random.randint(2, 4)
            ))
        else:
            self.sponsors.add(random.choice(Entity.objects.all()))

        # Set series
        # 50% chance of being in a series
        if random.randint(1, 2) == 1:
            self.series = random.choice(Series.objects.all())

        # Add sessions
        start_time = self.start.replace(microsecond=0, second=0, minute=0)
        number_of_sessions = random.randint(1, 10)
        for i in range(number_of_sessions):
            duration = random.choice([30, 60, 120, 180])
            end_time = start_time + timedelta(minutes=duration)
            for i in range(random.randint(1, 3)):
                session = Session.objects.create(
                    # TODO: Figure out how to use faker properly, as it doesn't evaluate here the standard way
                    name=faker.Faker().sentence(),
                    description=faker.Faker().paragraph(nb_sentences=10),
                    event=self,
                    url=faker.Faker().url(),
                    start=start_time,
                    end=end_time,
                )
                # Set location
                # 80% chance one location, otherwise multiple
                if random.randint(1, 5) == 1:
                    session.locations.add(*random.sample(
                        list(Location.objects.all()),
                        random.randint(2, 4)
                    ))
                else:
                    session.locations.add(random.choice(Location.objects.all()))
                session.save()
            # Set start time for next session as end time for this session
            start_time = end_time
        self.update_datetimes()
