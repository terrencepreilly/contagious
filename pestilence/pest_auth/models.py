""" `Profile` holds unique identifier information for a User """
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    @property
    def count(self):
        return self.contact_set.count()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create and save a `Profile` after User save. """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
