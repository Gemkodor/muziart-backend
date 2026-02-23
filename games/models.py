from django.db import models
from core.models import MusicNote, Profile

class Track(models.Model):
    title = models.CharField(max_length=255)
    secondary_title = models.CharField(max_length=255, blank=True, null=True)
    composer = models.CharField(max_length=255, blank=True, null=True)
    difficulty = models.IntegerField(default=1)
    filename = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title} ({self.composer})" if self.composer else self.title


class GameProgress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=50)
    current_level = models.IntegerField(default=1)
    max_score = models.IntegerField(default=0)

    
class ScrollingGame(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    nb_correct_answers = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Scrolling Game Level {self.current_level}"


class ScrollingGameLevel(models.Model):
    level_number = models.PositiveIntegerField(unique=True)
    notes = models.ManyToManyField(MusicNote)
    
    def __str__(self):
        return f"{self.level_number}"


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
