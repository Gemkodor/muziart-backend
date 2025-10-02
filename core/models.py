from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


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
    experience = models.IntegerField(default=0)
    streak_count = models.PositiveIntegerField(default=0)
    last_streak_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "Profil de {}".format(self.user.username)
    
    def get_level(self):
        return (self.experience // 100) + 1

    def get_current_level_xp_range(self):
        level = self.get_level()
        min_xp = (level - 1) * 100
        max_xp = level * 100
        return min_xp, max_xp

    def get_progression_ratio(self):
        min_xp, max_xp = self.get_current_level_xp_range()
        return (self.experience - min_xp) / (max_xp - min_xp)
    
    def update_streak(self):
        today = timezone.now().date()
        
        if self.last_streak_date == today:
            if self.streak_count == 0:
                # Streak starts
                self.streak_count = 1
            return
        
        if self.last_streak_date == today - timedelta(days=1):
            # Streak continues
            self.streak_count += 1
        else:
            # Streak is broken
            self.streak_count = 0
            
        self.last_streak_date = today
        
    def add_keys(self, amount: int):
        self.nb_keys += amount
        self.update_streak()
        self.save(update_fields=["nb_keys", "streak_count", "last_streak_date"])


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


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    chapter = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.chapter} - {self.title}"


class CompletedLesson(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="completed_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('profile', 'lesson')


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name
    

# Signals
# Create profile when a user is created

@receiver(post_save, sender=User)
def create_profile(sender, instance, using, raw, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()