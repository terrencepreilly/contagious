""" Test one-to-one link to User Model """
import uuid

from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Profile


class ProfileTest(TestCase):
    """ `Profile` """

    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'test')

    def test_profile_automatically_created(self):
        self.assertEqual(Profile.objects.count(), 1)

    def test_primary_key_is_uuid(self):
        profile = Profile.objects.first()
        self.assertTrue(isinstance(profile.pk, uuid.UUID))

    def test_profile_has_status_which_changes_over_time(self):
        profile = Profile.objects.first()
        self.assertTrue(profile.status is not None)
        self.assertEqual(profile.status, 'HEALTHY')
        profile.infect()
        self.assertEqual(profile.status, 'SICK')
