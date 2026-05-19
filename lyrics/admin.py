from django.contrib import admin
from .models import Song, LyricsProgress

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'profile', 'created_at')
    search_fields = ('title', 'artist')

@admin.register(LyricsProgress)
class LyricsProgressAdmin(admin.ModelAdmin):
    list_display = ('profile', 'song', 'lines_unlocked', 'last_studied')
