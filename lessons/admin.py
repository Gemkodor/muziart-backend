from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    list_display = ('title', 'slug', 'chapter', 'order')
