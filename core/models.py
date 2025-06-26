from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nb_keys = models.IntegerField(default=0)

    def __str__(self):
        return "Profil de {}".format(self.user.username)


# Signals
# Create profile when a user is created

@receiver(post_save, sender=User)
def create_profile(sender, instance, using, raw, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()