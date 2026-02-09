from django.urls import path
from .views import *

urlpatterns = [
    path('', lessons_list, name='lessons-list'),
    path('<slug:lesson_slug>', lesson, name='lesson'),
    path('<slug:lesson_slug>/complete/', complete_lesson, name='complete-lesson'),
    path('<slug:lesson_slug>/uncomplete/', uncomplete_lesson, name='uncomplete-lesson'),
]