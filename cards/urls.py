from django.urls import path
from .views import *

urlpatterns = [
    path('', get_cards, name='get_cards'),
    path('unlock', unlock_card, name='unlock_card'),
]