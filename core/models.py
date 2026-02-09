from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nb_keys = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    streak_count = models.PositiveIntegerField(default=0)
    last_streak_date = models.DateField(null=True, blank=True)
    current_scrolling_game_level = models.IntegerField(default=1)

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


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    category = models.ForeignKey(InstrumentCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='instruments')
    
    def __str__(self):
        return self.name


class ScrollingGameLevel(models.Model):
    level_number = models.PositiveIntegerField(unique=True)
    notes = models.ManyToManyField('MusicNote')
    
    def __str__(self):
        return f"{self.level_number}"


class NoteName(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name


class MusicNote(models.Model):
    note = models.ForeignKey(NoteName, on_delete=models.CASCADE)
    position = models.IntegerField()
    
    def __str__(self):
        return f"{self.note.name}{self.position}"
    

# Signals
# Create profile when a user is created

@receiver(post_save, sender=User)
def create_profile(sender, instance, using, raw, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()