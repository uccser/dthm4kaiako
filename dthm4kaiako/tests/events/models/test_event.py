"""Unit tests for event model"""

from users.models import (
    User,
)
from events.models import (
    Event,
    Series,
    Session,
    Location,
    EventRegistration,
    ParticipantType,
    Address
    )
from unittest import mock
import datetime
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from django.contrib.gis.geos import Point
import datetime

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventModelTests(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        Series.objects.all().delete()
        Session.objects.all().delete()
        Location.objects.all().delete()
        EventRegistration.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()

    # ----------------------- tests for update_datetimes -----------------------

    def test_update_datetimes__same_start_and_end_datetimes_two_sessions(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()

        Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2023, 2, 13, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 2, 13, 12, 30, 0, 00, pytz.utc),
            event=Event.objects.get(name="Security in CS"),
        )

        Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 2, 13, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 2, 13, 12, 30, 0, 00, pytz.utc),
            event=Event.objects.get(name="Security in CS"),
        )

        expected_start_datetime = Session.objects.get(event=event, name="session 1").start
        expected_end_datetime = Session.objects.get(event=event, name="session 2").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    def test_update_datetimes__different_times_same_day_two_sessions(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        session_1 = Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2023, 6, 24, 9, 0, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 6, 24, 12, 0, 0, 00, pytz.utc),
            event=event,
        )
        session_1.save()
        session_2 = Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 6, 24, 13, 0, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 6, 24, 16, 0, 0, 00, pytz.utc),
            event=event,
        )
        session_2.save()
        expected_start_datetime = session_1.start
        expected_end_datetime = session_2.end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    def test_update_datetimes__different_days_same_time_two_sessions(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        session_1 = Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2023, 2, 13, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 2, 13, 12, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_1.save()
        session_2 = Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 2, 13, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 2, 14, 12, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_2.save()
        expected_start_datetime = session_1.start
        expected_end_datetime = session_2.end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    def test_update_datetimes__different_start_and_end_datetimes_many_sessions(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            id=4,
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2020, 4, 15),
            end=datetime.datetime(2020, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        session_1 = Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2020, 4, 15, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2020, 4, 15, 12, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_1.save()
        session_2 = Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2020, 4, 16, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2020, 4, 16, 12, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_2.save()
        session_3 = Session.objects.create(
            name="session 3",
            description="some description",
            start=datetime.datetime(2020, 4, 16, 10, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2020, 4, 16, 12, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_3.save()

        expected_start_datetime = session_1.start
        expected_end_datetime = session_3.end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    def test_update_datetimes__same_start_and_end_datetimes_many_sessions(self):
        event = Event.objects.create(
            name="Intro to logic gates",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 1, 24),
            end=datetime.datetime(2023, 1, 24),
            accessible_online=False,
            published=True
        )
        event.save()
        session_1 = Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_1.save()
        session_2 = Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_2.save()
        session_3 = Session.objects.create(
            name="session 3",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_3.save()

        session_4 = Session.objects.create(
            name="session 4",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_4.save()
        session_5 = Session.objects.create(
            name="session 5",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_5.save()
        session_6 = Session.objects.create(
            name="session 6",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_6.save()
        expected_start_datetime = session_1.start
        expected_end_datetime = session_4.end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    def test_update_datetimes__different_times_same_day_many_sessions(self):
        event = Event.objects.create(
            name="Cryptocurrency - what is it?",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 4, 3),
            end=datetime.datetime(2023, 4, 10),
            accessible_online=False,
            published=True
        )
        event.save()
        session_1 = Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2023, 1, 24, 13, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 24, 17, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_1.save()
        session_2 = Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 1, 25, 9, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 25, 13, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_2.save()
        session_3 = Session.objects.create(
            name="session 3",
            description="some description",
            start=datetime.datetime(2023, 1, 26, 11, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 26, 15, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_3.save()
        session_4 = Session.objects.create(
            name="session 4",
            description="some description",
            start=datetime.datetime(2023, 1, 27, 14, 30, 0, 00, pytz.utc),
            end=datetime.datetime(2023, 1, 27, 16, 30, 0, 00, pytz.utc),
            event=event,
        )
        session_4.save()
        expected_start_datetime = session_1.start
        expected_end_datetime = session_4.end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    def test_update_datetimes__different_days_same_time_many_sessions(self):
        event = Event.objects.create(
            name="Resource jam!",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 2, 28),
            end=datetime.datetime(2023, 3, 3),
            accessible_online=False,
            published=True
        )
        Session.objects.create(
            name="session 3",
            start=datetime.datetime(2023, 3, 2, 14, 0, 0),
            end=datetime.datetime(2023, 3, 2, 16, 0, 0),
            event=event,
        )
        Session.objects.create(
            name="session 1",
            description="some description",
            start=datetime.datetime(2023, 2, 28, 14, 0, 0),
            end=datetime.datetime(2023, 2, 28, 16, 0, 0),
            event=event,
        )
        Session.objects.create(
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 3, 1, 14, 0, 0),
            end=datetime.datetime(2023, 3, 1, 16, 0, 0),
            event=event,
        )
        expected_start_datetime = Session.objects.get(event=event, name="session 1").start
        expected_end_datetime = Session.objects.get(event=event, name="session 3").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)

    # ----------------------- tests for get_absolute_url -----------------------

    def test_get_absolute_url__returns_url_of_event_on_website(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        expected_event_name_lowered = event.name.lower()
        expected_event_name = expected_event_name_lowered.replace(" ", "-")
        expected_url = '/events/event/{}/{}/'.format(event.id, expected_event_name)
        self.assertEqual(str(event.get_absolute_url()), expected_url)

    # ----------------------- tests for get_short_name -----------------------

    def test_get_short_name__in_series(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        self.assertEqual(str(event.get_short_name()), '{}: {}'.format(event.series.abbreviation, event.name))

    def test_get_short_name__not_in_series(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(str(event.get_short_name()), event.name)

    # ----------------------- tests for location_summary -----------------------

    def test_location_summary__multiple_locations(self):
        location_2 = Location.objects.create(
            id=2,
            room='Room 456',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-12, 149)
        )
        location_2.save()

        location_3 = Location.objects.create(
            id=3,
            room='Room 7',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-27, 188)
        )
        location_3.save()
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.locations.set([location_2, location_3])
        event.save()
        self.assertEqual(event.location_summary(), 'Multiple locations')

    def test_location_summary__one_location(self):
        location_1 = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location_1.save()
        event =  Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.locations.set([location_1])
        event.save()
        location = event.locations.get()
        city = location.city
        region = location.get_region_display()
        expected_summary_text = '{}, {}'.format(city, region)
        self.assertEqual(event.location_summary(), expected_summary_text)

    def test_location_summary__no_location(self):
        event = Event.objects.create(
            name="Zoom for Beginners",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 2, 14),
            end=datetime.datetime(2023, 3, 14),
            accessible_online=True,
            published=True
        )
        event.save()
        self.assertEqual(event.location_summary(), None)

    # ----------------------- tests for is_register_or_apply -----------------------

    def test_is_register_or_apply__event_is_register(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.is_register_or_apply, True)

    def test_is_register_or_apply__event_is_apply(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.is_register_or_apply, True)

    def test_is_register_or_apply__event_is_neither(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        self.assertEqual(event.is_register_or_apply, False)

    # ----------------------- tests for get_registration_button_text -----------------------

    def test_get_registration_button_text__event_is_register(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_registration_button_text, "Register to attend event")

    def test_get_registration_button_text__event_is_apply(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_registration_button_text, "Apply to attend event")

    def get_registration_button_text__event_is_neither(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        self.assertEqual(event.get_registration_button_text, "")

    # ---------------------------- tests for has_ended ----------------------------

    def test_has_ended__event_ended(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2020, 4, 15),
            end=datetime.datetime(2020, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        self.assertEqual(event.has_ended, True)

    def test_has_ended__event_has_not_ended(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24, 10, 0, 0),
            end=datetime.datetime(2023, 6, 26, 16, 0, 0),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.has_ended, False)

    # ------------------------ tests for get_event_type_short -----------------------

    def test_get_event_type_short__apply(self):
        event = Event.objects.create(
            id=2,
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short, "Apply")

    def test_get_event_type_short__register(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short, "Register")

    def test_get_event_type_short__invite_only(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.date(2023, 4, 15),
            end=datetime.date(2023, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short, "Invite only")
    
    def test_get_event_type_short__external_link(self):
        event = Event.objects.create(
            name="Intro to logic gates - part 2",
            description="description",
            registration_type=3,
            start=datetime.date(2023, 1, 24),
            end=datetime.date(2023, 1, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short, "External")

    # ------------------------ tests for get_event_type_short_updating -----------------------

    def test_get_event_type_short_updating__apply(self):
        event = Event.objects.create(
            id=2,
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.date(2023, 2, 13),
            end=datetime.date(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short_updating, "Update registration form")

    def test_get_event_type_short_updating__register(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short_updating, "Update registration form")

    def test_get_event_type_short_updating__invite_only(self):
        series_1 = Series.objects.create(
            id=1,
            name='Artificial Intelligence series',
            abbreviation='AI series',
            description='Some description',
        )
        series_1.save()
        event = Event.objects.create(
            name="Teaching with AI",
            description="description",
            registration_type=4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            series=series_1,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short_updating, "")
    
    def test_get_event_type_short_updating__external_link(self):
        event = Event.objects.create(
            id=9,
            name="Intro to logic gates - part 2",
            description="description",
            registration_type=3,
            start=datetime.datetime(2023, 1, 24),
            end=datetime.datetime(2023, 1, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(event.get_event_type_short_updating, "")

    # ----------------------------- tests for start_weekday_name -------------------

    def test_start_weekday_name__expected_weekday(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        expected_weekday = "Saturday"
        self.assertEqual(expected_weekday, event.start_weekday_name)

    # -------------------- tests for is_less_than_one_week_prior_event -------------

    def test_is_less_than_one_week_prior_event__one_week_prior_start_end_of_year(self):
        event_start_date = datetime.datetime(2023, 1, 1, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2022, 12, 31, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 1, 10, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            # Since one week prior start is 2022-12-31 10.21pm
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__one_week_prior_start_end_of_month(self):
        event_start_date = datetime.datetime(2023, 2, 28, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 2, 22, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            # Since one week prior start is 2023-01-31 10.21pm
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__one_week_prior_start(self):
        event_start_date = datetime.datetime(2023, 2, 18, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 2, 12, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 2, 20, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__two_weeks_prior_start(self):
        event_start_date = datetime.datetime(2023, 2, 24, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 2, 2, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertFalse(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__one_day_prior_start(self):
        event_start_date = datetime.datetime(2023, 1, 16, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 1, 15, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )

        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__same_datetime_as_start(self):
        event_start_date = datetime.datetime(2023, 1, 16, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 1, 16, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__one_week_after_start(self):
        event_start_date = datetime.datetime(2023, 1, 16, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 1, 23, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__two_weeks_after_start(self):
        event_start_date = datetime.datetime(2023, 1, 16, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 1, 30, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26,  10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertTrue(event.is_less_than_one_week_prior_event)

    def test_is_less_than_one_week_prior_event__one_day_after_start(self):
        event_start_date = datetime.datetime(2023, 1, 16, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        current_date = datetime.datetime(2023, 1, 17, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE)
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=event_start_date,
            end=datetime.datetime(2023, 6, 26, 10, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        with mock.patch('datetime.datetime') as mock_date:
            mock_date.today.return_value = current_date
            self.assertTrue(event.is_less_than_one_week_prior_event)


    # ----------------------------- tests for registration_status_counts ------------------------------

    def test_registration_status_counts__one_of_each(self):
        user_kate = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

        user_fiona = User.objects.create_user(
            id=2,
            username='fiona',
            first_name='Fiona',
            last_name='Apple',
            email='fiona@uclive.ac.nz',
            password='potato',
        )
        user_fiona.save()

        user_tori = User.objects.create_user(
            id=3,
            username='tori',
            first_name='Tori',
            last_name='Amos',
            email='tori@uclive.ac.nz',
            password='potato',
        )
        user_tori.save()

        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        registration_type_event_staff = ParticipantType.objects.create(
            name="Event staff",
            price=10.00
        )
        registration_type_event_staff.save()

        registration_type_teacher = ParticipantType.objects.create(
            name="Teacher",
            price=10.00
            )
        registration_type_teacher.save()

        registration_type_student = ParticipantType.objects.create(
            name="Student",
            price=10.00
            )
        registration_type_student.save()

        registration_type_student = ParticipantType.objects.create(
            name="Facilitator",
            price=10.00
            )
        registration_type_student.save()

        event_registration_1_pending = EventRegistration.objects.create(
            user=user_kate,
            event=event,
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz",
            participant_type = registration_type_event_staff
        )
        event_registration_1_pending.status = 1
        event_registration_1_pending.save()

        event_registration_2_approved = EventRegistration.objects.create(
            user=user_fiona,
            event=event,
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz",
            participant_type = registration_type_event_staff
        )
        event_registration_2_approved.status = 2
        event_registration_2_approved.save()

        event_registration_3_declined = EventRegistration.objects.create(
            user=user_tori,
            event=event,
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz",
            participant_type = registration_type_event_staff
        )
        event_registration_3_declined.status = 3
        event_registration_3_declined.save()

        expected_status_counts = {
            'pending': 1,
            'approved': 1,
            'declined': 1,
            'withdrawn': 0
        }
        self.assertEqual(expected_status_counts, event.registration_status_counts)
    
    
    def test_registration_status_counts__no_registrations(self):
        event = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        expected_status_counts = {
            'pending': 0,
            'approved': 0,
            'declined': 0,
            'withdrawn': 0
        }
        self.assertEqual(expected_status_counts, event.registration_status_counts)
    
    # ----------------------------- tests for participant_type_counts ------------------------------
    
    # ----------------------------- tests for reasons_for_withdrawing_counts ------------------------------
    
    # ----------------------------- tests for other_reasons_for_withdrawing ------------------------------

    # ----------------------------- tests for __str__ ------------------------------

    def test_str_representation(self):
        event = event_physical_register_1 = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True,
            capacity=10
        )
        event_physical_register_1.save()
        self.assertEqual(str(event), event.name)

    # --------------------------- tests for registration_status_counts ------------


    # ----------------------------- tests for capacity_percentage ------------------------------
    def test_capacity_percentage_capacity(self):
        user_kate = User.objects.create(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

        event_physical_register_1 = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True,
            capacity=10
        )
        event_physical_register_1.save()

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        participant_type = ParticipantType.objects.create(name="Teacher", price=10.00)
        participant_type.save()

        event_registration_1_pending = EventRegistration.objects.create(
            id=1,
            participant_type= participant_type,
            user=user_kate,
            event=event_physical_register_1,
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz"
        )
        approved = 2
        event_registration_1_pending.status = approved
        event_registration_1_pending.save()

        expected_result = float(10)
        self.assertEqual(event_physical_register_1.capacity_percentage, expected_result)
