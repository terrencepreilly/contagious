"""
Holds models which represent a single 'contact' between two
users.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from django.db.models.signals import m2m_changed

from pest_auth.models import Profile


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

    # change to a through table with profile
    profiles = models.ManyToManyField(
        Profile,
        help_text=('The (at most two) profiles involved in the contact.'),
        )

    @property
    def duration(self):
        """ The duration of time two users were near one another. """
        return self.end - self.start


def validate_profiles(sender, **kwargs):
    msg = 'At most two profiles can be involved in a contact.'
    action = kwargs.get('action', None)
    instance = kwargs.get('instance', None)
    if action == 'pre_add' and isinstance(instance, Contact):
        if instance.profiles.count() == 2:
            raise ValidationError(msg)

m2m_changed.connect(validate_profiles, sender=Contact.profiles.through)
