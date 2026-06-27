from django.contrib import admin
from .models import Track, Instrument, InstrumentCategory

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "secondary_title", "composer", "filename", "difficulty")


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'image_name', 'image_url')
    list_filter = ('category',)
    search_fields = ('name',)
    fields = ('name', 'category', 'level', 'image_url', 'image_name')


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)