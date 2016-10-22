""" Model tests """
from datetime import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase

from ..models import (
    Contact,
    )


class ContactModelTest(TestCase):
    """ Contacts represent a single 'contact' between two people. """

    def test_duration(self):
        """ duration() should give the time between the end and start """
        contact = Contact(
            start=datetime(2001, 1, 1, 0, 0, 0),
            end=datetime(2001, 1, 1, 4, 30, 5),
            )

        expected_seconds = float(4*60**2 + 30*60 + 5)

        self.assertEqual(
            contact.duration.total_seconds(),
            expected_seconds,
            'Duration() should give the time between end and start.'
            )

    def test_only_two_profiles_can_be_added(self):
        """ Only at most two profiles should be able to be added ever. """

        def create_user(number):  # pylint:disable=missing-docstring
            name = 'test{}'.format(number)
            user = User.objects.create_user(
                name,
                name + '@example.com',
                name + 'password',
                )
            return user.profile

        profile1 = create_user(1)
        profile2 = create_user(2)
        profile3 = create_user(3)

        contact = Contact.objects.create(  # pylint:disable=no-member
            start=datetime(2001, 1, 1, 0, 0, 0),
            end=datetime(2001, 1, 1, 4, 30, 5),
            )
        contact.profiles.add(profile1)
        contact.profiles.add(profile2)

        with self.assertRaises(ValidationError):
            contact.profiles.add(profile3)
