from django.test import TestCase
from events.forms import EventregistrationForm
from http import HTTPStatus
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from unittest import mock


class EventregistrationFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            'user',
            'user@dthm4kaiako.ac.nz',
            password="password",
            first_name='Alex',
            last_name='Doe'
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True
        )

    def test_required_fields_only(self):
        pass

    # TODO: figure out how to do integration tests for forms in views and mocking the existing event and checking
    # the data coming through is as expected and results in the right response status code
    @mock.patch('events.views.requests')
    def test_successful_event_registration_form(self, mock_requests):
        event_id = 1
        self.client.login(id=1, password='password')
        mock_requests.get.return_value.status_code = 200
        response = self.client.post(f"/events/register/{event_id}/", data={})  # TODO:  add data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Post code must be four digits.", html=True)

    # -------------------------------------- Validating form tests -------------------------

    def test_validating_valid_form(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(event_registration_form.errors, {})

    def test_invalid_participant_type_integer_gives_error(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            "participant_type": 16,
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors['participant_type'],
            ['Select a valid choice. That choice is not one of the available choices.']
        )

    def test_invalid_participant_type_string_gives_error(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            "participant_type": "20",
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors['participant_type'],
            ['Select a valid choice. That choice is not one of the available choices.']
        )

    def test_invalid_participant_type_string_type_gives_error(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            "participant_type": "Teacher",
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors['participant_type'],
            ['Select a valid choice. That choice is not one of the available choices.']
        )

    def test_invalid_emergency_contact_first_name__too_long(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'Johnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_first_name"],
            ["Ensure this value has at most 50 characters (it has 51)."]
        )

    def test_invalid_emergency_contact_last_name__too_long(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jonesssssssssssssssssssssssssssssssssssssssssssssss",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_last_name"],
            ["Ensure this value has at most 50 characters (it has 51)."]
        )

    def test_invalid_emergency_contact_relationship__too_long(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship":
                (
                    "My sister's friend's brother's girl friend's dog's breeder's mother's sister's professional"
                    " lawn mower who comes on Tuesdays, Thursdays and Sundays that has a floppy hat."
                ),
                "emergency_contact_phone_number": "123456789"
                }
            )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_relationship"],
            ["Ensure this value has at most 150 characters (it has 170)."]
        )

    def test_invalid_emergency_contact_phone_number__invalid_symbols(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "!@*/&()"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            [
                'Phone number can include the area code, follow by any number of numbers, '
                '- and spaces. E.g. (+64) 123 45 678, 123-45-678, 12345678'
            ]
        )

    def test_invalid_emergency_contact_phone_number__plus_integers_and_spaces(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "+64 8392 292 53"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            {}
        )

    def test_invalid_emergency_contact_phone_number__plus_brackets_integers_and_spaces(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "(+64) 8392 292 53"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            {}
        )

    def test_invalid_emergency_contact_phone_number__plus_brackets_integers_dashes_and_spaces(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "(+64) 8392-292-53"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            {}
        )

    def test_invalid_emergency_contact_phone_number__plus_brackets_and_integers(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "(+64) 839229253"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            {}
        )

    def test_invalid_emergency_contact_phone_number__plus_brackets_and_integers_no_spaces(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_first_name": 'John',
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "(+64)839229253"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            {}
        )

    def test_missing_emergency_contact_first_name(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
            # "participant_type": ParticipantType.objects.get(name="Teacher"),
            "emergency_contact_last_name": "Jones",
            "emergency_contact_relationship": "Friend",
            "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_first_name"],
            ['This field is required.']
        )

    def test_missing_emergency_contact_relationship(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
                # "participant_type": ParticipantType.objects.get(name="Teacher"),
                "emergency_contact_first_name": 'John',
                "emergency_contact_last_name": "Jones",
                "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_relationship"],
            ['This field is required.']
        )

    def test_missing_emergency_contact_phone_number(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
                # "participant_type": ParticipantType.objects.get(name="Teacher"),
                "emergency_contact_first_name": 'John',
                "emergency_contact_last_name": "Jones",
                "emergency_contact_relationship": "Friend",
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_phone_number"],
            [
                'This field is required.',
                (
                    'Phone number can include the area code, follow by any number of numbers,'
                    ' - and spaces. E.g. (+64) 123 45 678, 123-45-678, 12345678'
                )
            ]
        )

    def test_missing_emergency_contact_last_name(self):
        # generate_participant_types()
        event_registration_form = EventregistrationForm(data={
                # "participant_type": ParticipantType.objects.get(name="Teacher"),
                "emergency_contact_first_name": 'John',
                "emergency_contact_relationship": "Friend",
                "emergency_contact_phone_number": "123456789"
            }
        )
        self.assertEqual(
            event_registration_form.errors["emergency_contact_last_name"],
            ['This field is required.']
        )
