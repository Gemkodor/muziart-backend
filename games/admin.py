from django.contrib import admin
from .models import Track

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "secondary_title", "composer", "filename", "difficulty")