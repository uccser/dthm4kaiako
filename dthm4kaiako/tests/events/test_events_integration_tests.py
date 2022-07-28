from django.test import TestCase
from http import HTTPStatus
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from unittest import mock
from django.test.client import Client
from unittest import mock

# TODO: resolve all these failing tests!

class AddEventApplicationViewTests(TestCase):

    def test_get(self):
        client = Client()
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

        self.client.login(id=1, password='password')
        response = self.client.get("/events/register/1/")


        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.status_code = 200
            # mock_get.return_value.text = 'Bad Request El'

        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    # TODO: need to log in
    def test_post_success(self):
        event_name = "CSSE BBQ"
        event_id = 1
        response = self.client.post(f"/events/register/{event_id}/", data={
            'first_name': "Bob",
            'last_name': "Ross",
            'region': "14",
            'educational_entities': "4",
            'medical_notes': "some notes here",
            'email_address': "test@gmail.com",
            'email_address_confirm': "test@gmail.com",
            'mobile_phone_number': "012345678",
            'mobile_phone_number_confirm': "012345678",
            'participant_type': "3",
            'emergency_contact_first_name': "Rob",
            'emergency_contact_last_name': "Smith",
            'emergency_contact_relationship': "Friend",
            'emergency_contact_phone_number': "1234567",
            'street_number': "1",
            'street_name': "Some street",
            'suburb': "Some suburb",
            'city': "Christchurch",
            'region': "14",
            'post_code': 8041,
            'country': "New Zealand",
            'bill_to': "University of Canterbury",
            'billing_email_address': "testtest@test.com",
            'I_agree_to_the_terms_and_conditions': "on"
        })
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], f"/events/register/{event_id}/{event_name}/")

    # TODO: need to log in
    def test_post_error(self):
        event_id = 1
        response = self.client.post(f"/events/register/{event_id}/", data={
            'first_name': "Bobbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Use 'and' instead of '&'", html=True)