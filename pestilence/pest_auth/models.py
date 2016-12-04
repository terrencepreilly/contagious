""" `Profile` holds unique identifier information for a User """
from datetime import timedelta
from random import Random
import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import fields
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """ The user's profile -- for identification. """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=('The unique identifier for our user. Since '
                   'Java\'s UUID class also follows RFC 4122, '
                   'there should be no problems using this id '
                   'on both systems.')
        )
    start_sickness = ArrayField(
        fields.DateTimeField(
            null=False,
            blank=False,
            default=None,
            ),
        blank=True,
        default=list,
        help_text=('The time a person started being sick.'),
        )
    end_sickness = ArrayField(
        fields.DateTimeField(
            null=False,
            blank=False,
            default=None,
            ),
        blank=True,
        default=list,
        help_text=('The time a person stoped being sick.'),
        )

    @property
    def sick(self):
        if len(self.start_sickness) == 0:
            return False
        now = timezone.now()
        return self.start_sickness[-1] < now < self.end_sickness[-1]

    @property
    def status(self):
        if self.sick:
            return 'SICK'
        return 'HEALTHY'

    @property
    def count(self):
        return self.contact_set.count()

    @property
    def sickdays(self):
        """Calculates the total amount of time this user was sick."""
        total_seconds = 0
        for i in range(len(self.start_sickness)):
            seconds = (self.end_sickness[i]
                       - self.start_sickness[i]).total_seconds()
            total_seconds += seconds
        return round(total_seconds / (60 * 60 * 24))

    def infect(self):
        """Makes one sick from now until somewhere between 2 and 27
        hours from now."""
        rand = Random()
        diff = timedelta(seconds=rand.randint(10**4, 10**5))
        self.start_sickness.append(timezone.now())
        self.end_sickness.append(timezone.now() + diff)
        self.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create and save a `Profile` after User save. """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
