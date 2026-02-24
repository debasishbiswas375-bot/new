from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create profile ONLY when user is first created.
    This prevents infinite loop and 502 error during delete.
    """
    if created:
        UserProfile.objects.create(user=instance)
