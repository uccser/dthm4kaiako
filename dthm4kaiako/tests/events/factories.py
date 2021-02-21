"""Module for factories for testing the events application."""

import random
import pytz
import datetime
from datetime import timedelta
from tests.utils import random_boolean, random_event_application_status
from factory import DjangoModelFactory, Faker, post_generation, LazyFunction, LazyAttribute, Iterator
from factory.faker import faker
from users.models import Entity
from events.models import (
    Series,
    Event,
    Location,
    Session,
    RegistrationForm,
    EventApplication,
    ApplicantType,
    EventVoucher,
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
    published = True
    start = Faker('date_time_between', start_date='-1y', end_date='+3y', tzinfo=pytz.timezone('Pacific/Auckland'))
    end = LazyAttribute(lambda obj: obj.start)
    accessible_online = LazyFunction(random_boolean)

    class Meta:
        """Metadata for class."""

        model = Event

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add detail to event."""
        FAKER = faker.Faker()

        # Set registration_link
        # 20% chance
        if random.randint(1, 5) == 1:
            self.registration_link = FAKER.url()

        # Set featured
        # 20% chance
        if random.randint(1, 5) == 1:
            self.featured = True

        # Set show schedule
        # 50% chance
        if random.randint(1, 2) == 1:
            self.show_schedule = True

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
            Session.objects.create(
                name=FAKER.sentence(),
                description=FAKER.paragraph(nb_sentences=10),
                event=self,
                url=FAKER.url(),
                start=start_time,
                end=end_time,
            )
            start_time = end_time
        self.update_datetimes()

        # Add applicant types
        for name in ['Staff', 'Attendee', 'Vendor']:
            ApplicantType.objects.create(
                name=name,
                cost=random.randint(0, 250),
                event=self,
            )

        # 20% chance of event voucher
        if random.randint(1, 5) == 1:
            code = FAKER.lexify(text='??????')
            discount = random.choice([10, 20, 30, 40, 50])
            name = f"{discount}% discount"
            EventVoucher.objects.create(
                name=name,
                code=code,
                active=True,
                discount=discount,
                event=self,
            )


class RegistrationFormFactory(DjangoModelFactory):
    """Factory for generating registration forms."""

    datetime_open = datetime.datetime.now()
    datetime_end = datetime_open + timedelta(days=7)
    terms_and_conditions = Faker('paragraph', nb_sentences=50)
    event = Iterator(Event.objects.filter(registration_link=''))

    class Meta:
        """Metadata for class."""

        model = RegistrationForm
