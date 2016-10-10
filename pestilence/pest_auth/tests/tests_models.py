""" Test one-to-one link to User Model """
from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Profile


class ProfileTest(TestCase):
    """ `Profile` """

    def test_profile_automatically_created(self):
        User.objects.create_user('test', 'test@test.com', 'test')
        self.assertEqual(Profile.objects.count(), 1)
