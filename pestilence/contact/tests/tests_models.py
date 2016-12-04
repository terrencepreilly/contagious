""" Model tests """
from datetime import (
    datetime,
    timedelta,
    )

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

import pytz

from ..models import (
    Contact,
    )
from pest_auth.models import (
    Profile,
    )


class ContactModelTest(TestCase):
    """ Contacts represent a single 'contact' between two people. """

    def test_duration(self):
        """ duration() should give the time between the end and start """
        contact = Contact(
            start=datetime(2001, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            end=datetime(2001, 1, 1, 4, 30, 5, tzinfo=pytz.UTC),
            )

        expected_seconds = float(4*60**2 + 30*60 + 5)

        self.assertEqual(
            contact.duration.total_seconds(),
            expected_seconds,
            'Duration() should give the time between end and start.'
            )

    def create_user(self, number):  # pylint:disable=missing-docstring
        name = 'test{}'.format(number)
        user = User.objects.create_user(
            name,
            name + '@example.com',
            name + 'password',
            )
        return user.profile

    def refresh_profile(self, profile):  # pylint:disable=missing-docstring
        return Profile.objects.get(profile.uuid)

    def test_only_two_profiles_can_be_added(self):
        """ Only at most two profiles should be able to be added ever. """

        profile1 = self.create_user(1)
        profile2 = self.create_user(2)
        profile3 = self.create_user(3)

        contact = Contact.objects.create(
            start=datetime(2001, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            end=datetime(2001, 1, 1, 4, 30, 5, tzinfo=pytz.UTC),
            )
        contact.profiles.add(profile1)
        contact.profiles.add(profile2)

        with self.assertRaises(ValidationError):
            contact.profiles.add(profile3)

    def test_adding_sick_person_to_contact_infects_other(self):
        """ Sickness spreads automatically. """
        profile1 = self.create_user(1)
        profile2 = self.create_user(2)
        profile1.infect()
        contact = Contact.objects.create(
            start=timezone.now(),
            end=timezone.now() + timedelta(seconds=18000),
            )
        contact.profiles.add(profile1)
        contact.profiles.add(profile2)
        profile2 = Profile.objects.get(uuid=profile2.uuid)
        self.assertEqual(profile2.status, 'SICK')

    def test_adding_healthy_people_to_contact_does_not_infect(self):
        """ Sickness doesn't spawn randomly. """
        profile1 = self.create_user(1)
        profile2 = self.create_user(2)
        contact = Contact.objects.create(
            start=timezone.now(),
            end=timezone.now() + timedelta(seconds=18000),
            )
        contact.profiles.add(profile1)
        contact.profiles.add(profile2)
        self.assertTrue(all(
            [x.status == 'HEALTHY' for x in contact.profiles.all()]
            ))
