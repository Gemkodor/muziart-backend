from django.db import models
from core.models import Profile

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