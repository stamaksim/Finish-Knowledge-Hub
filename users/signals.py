from django.db.models.signals import post_save
from django.dispatch import receiver
from knowhub.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("Creating new profile...")
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print("Updating profile...")
    if hasattr(instance, 'profile'):
        instance.profile.save()
