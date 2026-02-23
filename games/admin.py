from django.contrib import admin
from .models import Track, Instrument, InstrumentCategory, ScrollingGame, ScrollingGameLevel

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "secondary_title", "composer", "filename", "difficulty")

   
@admin.register(Instrument)
class Instrument(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_name', 'level')
    

@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ScrollingGameLevel)
class ScrollingGameLevelAdmin(admin.ModelAdmin):
    list_display = ('level_number',)


@admin.register(ScrollingGame)
class ScrollingGameAdmin(admin.ModelAdmin):
    list_display = ('profile', 'current_level', 'nb_correct_answers')