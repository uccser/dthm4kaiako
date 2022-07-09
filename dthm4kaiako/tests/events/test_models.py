"""Unit tests for events"""

from django.test import TestCase
from django.contrib.auth.models import User
from events.models import (
    Event, 
    ApplicantType,
    Address,
    EventApplication,
    Series,
    Session,
    Location,
    RegistrationForm
    )
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_applicant_types,
    generate_event_registration_forms,
    generate_addresses,
    generate_event_applications,
    generate_serieses,
    generate_sessions
)


class EventModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_serieses()
        generate_locations()
        generate_events()
        generate_sessions()

    @classmethod
    def tearDownTestData(cls):
        Series.objects.all().delete()
        Event.objects.all().delete()
        Location.objects.all().delete()
        Session.objects.all().delete()


    # ----------------------- tests for update_datetimes -----------------------

    def test_update_datetimes__same_start_and_end_datetimes_two_sessions(self):
        event = Event.objects.get(id=2)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=2), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=2), name="session 2").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    def test_update_datetimes__different_times_same_day_two_sessions(self):
        event = Event.objects.get(id=1)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=1), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=1), name="session 2").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    def test_update_datetimes__different_days_same_time_two_sessions(self):
        event = Event.objects.get(id=3)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=3), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=3), name="session 2").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    def test_update_datetimes__different_start_and_end_datetimes_many_sessions(self):
        event = Event.objects.get(id=4)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=4), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=4), name="session 3").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    def test_update_datetimes__same_start_and_end_datetimes_many_sessions(self):
        event = Event.objects.get(id=5)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=5), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=5), name="session 4").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    def test_update_datetimes__different_times_same_day_many_sessions(self):
        event = Event.objects.get(id=6)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=6), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=6), name="session 4").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    def test_update_datetimes__different_days_same_time_many_sessions(self):
        event = Event.objects.get(id=7)
        expected_start_datetime = Session.objects.get(event=Event.objects.get(id=7), name="session 1").start
        expected_end_datetime = Session.objects.get(event=Event.objects.get(id=7), name="session 3").end
        event.update_datetimes()
        self.assertEqual(event.start, expected_start_datetime)
        self.assertEqual(event.end, expected_end_datetime)


    # ----------------------- tests for get_absolute_url -----------------------

    def test_get_absolute_url__returns_url_of_event_on_website(self):
        event = Event.objects.get(id=1)
        expected_event_name_lowered = event.name.lower()
        expected_event_name = expected_event_name_lowered.replace(" ","-")
        expected_url = '/events/event/{}/{}/'.format(event.id, expected_event_name)
        self.assertEqual(str(event.get_absolute_url()), expected_url)


    # ----------------------- tests for get_short_name -----------------------

    def test_get_short_name__in_series(self):
        event = Event.objects.get(id=3)
        self.assertEqual(str(event.get_short_name()), '{}: {}'.format(event.series.abbreviation, event.name))

    def test_get_short_name__not_in_series(self):
        event = Event.objects.get(id=1)
        self.assertEqual(str(event.get_short_name()), event.name)


    # ----------------------- tests for location_summary -----------------------

    def test_location_summary__multiple_locations(self):
        event = Event.objects.get(id=2)
        self.assertEqual(event.location_summary(), 'Multiple locations')

    def test_location_summary__one_location(self):
        event = Event.objects.get(id=1)
        location = event.locations.get()
        city = location.city
        region = location.get_region_display()
        expected_summary_text = '{}, {}'.format(city, region)
        self.assertEqual(event.location_summary(), expected_summary_text)

    def test_location_summary__no_location(self):
        event = Event.objects.get(id=8)
        self.assertEqual(event.location_summary(), None)


    # ----------------------- tests for is_register_or_apply -----------------------

    def test_is_register_or_apply__event_is_register(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.is_register_or_apply, True)

    def test_is_register_or_apply__event_is_apply(self):
        event = Event.objects.get(id=2)
        self.assertEqual(event.is_register_or_apply, True) 
        
    def test_is_register_or_apply__event_is_neither(self):
        event = Event.objects.get(id=3)
        self.assertEqual(event.is_register_or_apply, False) 


    # ---------------------------- tests for has_ended ----------------------------

    def test_has_ended__event_ended(self):
        event = Event.objects.get(id=4)
        self.assertEqual(event.has_ended, True)  

    def test_has_ended__event_has_not_ended(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.has_ended, False)  


    # ------------------------ tests for get_event_type_short -----------------------

    def test_get_event_type_short__apply(self):
        event = Event.objects.get(id=2)
        self.assertEqual(event.get_event_type_short, "Apply")

    def test_get_event_type_short__register(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.get_event_type_short, "Register") 


    # ------------------------ tests for has_attendance_fee -----------------------

    def test_has_attendance_fee__event_has_fee(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.has_attendance_fee, True) 

    def test_has_attendance_fee__event_is_free(self):
        event = Event.objects.get(id=3)
        self.assertEqual(event.has_attendance_fee, False)  


    # ----------------------------- tests for __str__ ------------------------------

    def test_str_representation(self):
        event = Event.objects.get(id=1)
        self.assertEqual(str(event), event.name)


class ApplicantTypeTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_applicant_types()

    @classmethod
    def tearDownTestData(cls):
        ApplicantType.objects.all().delete()

    # ----------------------------- tests for __str__ ------------------------------

    def test_str_representation__register(self):
        test_name = "Event staff"
        application_type = ApplicantType.objects.get(name=test_name)
        self.assertEqual(str(application_type), application_type.name)


class AddressTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_addresses()
        generate_users()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_applicant_types()
        generate_event_applications()


    @classmethod
    def tearDownTestData(cls):
        EventApplication.objects.all().delete()
        ApplicantType.objects.all().delete()
        Series.objects.all().delete()
        Event.objects.all().delete()
        Location.objects.all().delete()
        User.objects.all().delete()
        Address.objects.all().delete()


    # ------------------------------- tests for __str__ ----------------------------

    def test_str_representation(self):
        application = EventApplication.objects.get(id=1)
        billing_address = application.billing_physical_address
        self.assertEqual(str(billing_address),
        '{} {},\n{},\n{},\n{}'.format(billing_address.street_number, billing_address.street_name, billing_address.suburb, billing_address.city, billing_address.post_code)) 
 

    # ---------------------------- tests for get_full_address ----------------------

    def test_get_full_address(self):
        application = EventApplication.objects.get(id=1)
        billing_address = application.billing_physical_address
        self.assertEqual(str(billing_address.get_full_address()),
        '{} {},\n{},\n{},\n{}'.format(billing_address.street_number, billing_address.street_name, billing_address.suburb, billing_address.city, billing_address.post_code)) 
 

class EventApplicationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_applicant_types()
        generate_event_applications()

    @classmethod
    def tearDownTestData(cls):
        Address.objects.all().delete()
        Series.objects.all().delete()
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()
        ApplicantType.objects.all().delete()
        EventApplication.objects.all().delete()

    # ------------------------------- tests for status_string_for_user ----------------------------

    def test_status_string_for_user__pending(self):
        event_application = EventApplication.objects.get(id=1)
        self.assertEqual(event_application.status_string_for_user, "Pending") 

    def test_status_string_for_user__approved(self):
        event_application = EventApplication.objects.get(id=2)
        self.assertEqual(event_application.status_string_for_user, "Approved") 

    def test_status_string_for_user__rejected(self):
        event_application = EventApplication.objects.get(id=3)
        self.assertEqual(event_application.status_string_for_user, "Rejected") 

    def test_status_string_for_user__withdrawn(self):
        event_application = EventApplication.objects.get(id=4)
        self.assertEqual(event_application.status_string_for_user, "Withdrawn") 

    
    # ------------------------------- tests for withdraw ------------------------------

    def test_withdraw__not_already_withdrawn(self):
        event_application = EventApplication.objects.get(id=1)
        event_application.withdraw()
        self.assertEqual(event_application.status, 4) 

    def test_withdraw__already_withdrawn(self):
        event_application = EventApplication.objects.get(id=4)
        self.assertEqual(event_application.status, 4) 


class RegistrationFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        generate_applicant_types()
        generate_event_applications()

    @classmethod
    def tearDownTestData(cls):
        Address.objects.all().delete()
        Series.objects.all().delete()
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()
        ApplicantType.objects.all().delete()
        EventApplication.objects.all().delete()

    # ------------------------------- tests for get_absolute_url ------------------------------

    def test_get_absolute_url__returns_url_of_registration_form_on_website(self):
        reg_form = RegistrationForm.objects.get(event_id=1)
        event = reg_form.event 
        event_pk = event.pk
        event_slug = event.slug
        expected_url = '/events/register/{}/'.format(event_pk)
        self.assertEqual(str(reg_form.get_absolute_url()), expected_url)

