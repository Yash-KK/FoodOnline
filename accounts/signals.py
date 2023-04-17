from django.db.models.signals import post_save
from django.dispatch import receiver

#MODELS
from .models import (
    User,
    UserProfile
)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()        
    else:
        try:
            instance.user_profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)