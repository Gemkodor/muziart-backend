from django.db import models
from core.models import Profile


class DailyProgram(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='daily_programs')
    date = models.DateField()
    time_goal = models.PositiveIntegerField()  # minutes

    class Meta:
        unique_together = ('profile', 'date')

    def __str__(self):
        return f"{self.profile} — {self.date} ({self.time_goal} min)"

    @property
    def completed(self):
        return self.activities.filter(completed=False).count() == 0

    @property
    def done_count(self):
        return self.activities.filter(completed=True).count()

    @property
    def total_count(self):
        return self.activities.count()


class DailyActivity(models.Model):
    TYPES = [
        ('lesson',         'Cours'),
        ('notes_reading',  'Lecture de notes'),
        ('blind_test',     'Blind test'),
        ('scales_builder', 'Construction de gammes'),
    ]

    program = models.ForeignKey(DailyProgram, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=TYPES)
    activity_ref = models.CharField(max_length=100, blank=True)   # lesson slug or ''
    activity_title = models.CharField(max_length=150)
    estimated_minutes = models.PositiveIntegerField(default=3)
    order = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['order']
