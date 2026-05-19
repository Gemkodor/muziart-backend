from django.db import models
from core.models import Profile


class Song(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True)
    lyrics = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.artist}" if self.artist else self.title


class LyricsProgress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='lyrics_progress')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='progress')
    lines_unlocked = models.PositiveIntegerField(default=0)
    last_studied = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('profile', 'song')

    def __str__(self):
        return f"{self.profile} — {self.song.title} ({self.lines_unlocked} lines)"
