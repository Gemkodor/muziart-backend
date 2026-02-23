from django.contrib import admin
from .models import Profile, MusicNote, NoteName


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nb_keys', 'experience', 'streak_count', 'last_streak_date', 'current_scrolling_game_level')


@admin.register(MusicNote)
class MusicNoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'position')


@admin.register(NoteName)
class NoteNameAdmin(admin.ModelAdmin):
    list_display = ('name',)