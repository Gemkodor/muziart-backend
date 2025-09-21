from django.db import models


class Track(models.Model):
    title = models.CharField(max_length=255)
    secondary_title = models.CharField(max_length=255, blank=True, null=True)
    composer = models.CharField(max_length=255, blank=True, null=True)
    difficulty = models.IntegerField(default=1)
    filename = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title} ({self.composer})" if self.composer else self.title
    