"""
Holds models which represent a single 'contact' between two
users.
"""

from django.db import models
from django.db.models import fields


class Contact(models.Model):
    """ A single contact between two users. """
    start = fields.DateTimeField(
        null=False,
        blank=False,
        default=None,
        help_text=('The recorded start of an uninterrupted period '
                   'of contact between two users.'),
        )
    end = fields.DateTimeField(
        null=False,
        blank=False,
        default=None,
        help_text=('The recorded end of an uninterrupted period '
                   'of contact between two users.'),
        )

    @property
    def duration(self):
        """ The duration of time two users were near one another. """
        return self.end - self.start
