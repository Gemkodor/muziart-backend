from django.db import models
from core.models import Profile


class Quest(models.Model):
    QUEST_TYPES = [
        ('read_lesson', 'Lire des cours'),
        ('play_notes_reading', 'Jouer à Lecture de notes'),
    ]

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    quest_type = models.CharField(max_length=40, choices=QUEST_TYPES)
    required_count = models.PositiveIntegerField(default=1)
    xp_reward = models.PositiveIntegerField(default=10)
    keys_reward = models.PositiveIntegerField(default=2)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class UserQuest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_quests')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='user_quests')
    progress = models.PositiveIntegerField(default=0)
    claimed = models.BooleanField(default=False)
    claimed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('profile', 'quest')

    @property
    def completed(self):
        return self.progress >= self.quest.required_count
