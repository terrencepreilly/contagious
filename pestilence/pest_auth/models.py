""" `Profile` holds unique identifier information for a User """

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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create and save a `Profile` after User save. """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
