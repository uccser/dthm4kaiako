"""Unit tests for events"""

from django.test import TestCase
from django.contrib.auth.models import User
from events.models import (
    Event, 
    ApplicantType,
    Address,
    EventApplication,
    )
from tests.dthm4kaiako_test_data_generator import (
    generate_users,
    generate_events,
    generate_applicant_types,
    generate_event_registration_forms,
    generate_addresses,
    generate_event_applications,
)


class EventModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_events()

    @classmethod
    def tearDownTestData(cls):
        Event.objecs.all().delete()

    # ----------------------- tests for update_datetimes -----------------------

    #TODO: write unit tests

    # ----------------------- tests for get_absolute_url -----------------------

    #TODO: write unit tests

    # ----------------------- tests for get_short_name -----------------------

    #TODO: write unit tests

    # ----------------------- tests for location_summary -----------------------

    #TODO: write unit tests

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
        ApplicantType.objecs.all().delete()

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
        generate_events()
        generate_applicant_types()
        generate_event_applications()


    @classmethod
    def tearDownTestData(cls):
        EventApplication.objects.all().delete()
        ApplicantType.objects.all().delete()
        Event.objects.all().delete()
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
        generate_event_registration_forms()

    @classmethod
    def tearDownTestData(cls):
        EventApplication.objecs.all().delete()

    # ------------------------------- tests for status_string_for_user ----------------------------

    def test_status_string_for_user__pending(self):
        pass 

    def test_status_string_for_user__approved(self):
        pass 

    def test_status_string_for_user__rejected(self):
        pass 

    def test_status_string_for_user__withdrawn(self):
        pass 

    
    # ------------------------------- tests for withdraw ------------------------------

    def test_withdraw__not_already_withdrawn(self):
        pass 

    def test_withdraw__already_withdrawn(self):
        pass 

    
    # ------------------------------- tests for get_absolute_url ------------------------------

    def test_get_absolute_url(self):
        pass 
