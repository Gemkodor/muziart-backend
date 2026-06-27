from django.contrib import admin
from .models import Track, Instrument, InstrumentCategory

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "secondary_title", "composer", "filename", "difficulty")


@admin.register(Instrument)
class Instrument(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_name', 'level')


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)