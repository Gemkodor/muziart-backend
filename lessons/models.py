from django.db import models
from core.models import Profile

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