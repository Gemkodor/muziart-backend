from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class CollectionCategory(models.Model):
    CATEGORY_CHOICES = [
        ('composer', 'Compositeur'),
        ('instrument', 'Instrument')
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='composer')
    
    def __str__(self):
        return f"{self.name}"


class CardRarity(models.Model):
    RARITY_CHOICES = [
        ('common', 'Commun'),
        ('rare', 'Rare'),
        ('epic', 'Légendaire')
    ]
    name = models.CharField(max_length=100, choices=RARITY_CHOICES, default='common')
    
    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nb_keys = models.IntegerField(default=0)

    def __str__(self):
        return "Profil de {}".format(self.user.username)


class Card(models.Model):
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    category = models.ForeignKey(CollectionCategory, on_delete=models.CASCADE)
    rarity = models.ForeignKey(CardRarity, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price_to_unlock = models.IntegerField(default=5)
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class ProfileCard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='profile_cards')
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('profile', 'card')
        
    def __str__(self):
        return f"{self.profile.user.username} - {self.card.name}"


# Signals
# Create profile when a user is created

@receiver(post_save, sender=User)
def create_profile(sender, instance, using, raw, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()