""" Model tests """
from datetime import datetime

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
