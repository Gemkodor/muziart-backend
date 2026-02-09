from django.contrib import admin
from .models import Profile, Instrument, InstrumentCategory, ScrollingGameLevel, MusicNote, NoteName


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nb_keys', 'experience', 'streak_count', 'last_streak_date', 'current_scrolling_game_level')


@admin.register(Instrument)
class Instrument(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_name', 'level')
    

@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ScrollingGameLevel)
class ScrollingGameLevelAdmin(admin.ModelAdmin):
    list_display = ('level_number',)


@admin.register(MusicNote)
class MusicNoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'position')


@admin.register(NoteName)
class NoteNameAdmin(admin.ModelAdmin):
    list_display = ('name',)