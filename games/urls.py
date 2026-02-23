from django.urls import path
from . import views

urlpatterns = [
    # Blind test's urls
    path("blind-test/tracks/random/<int:nb_questions>/", views.random_track, name="random-track"),
    
    # Scrolling game's urls
    path('scrolling-game/level/<int:level_number>/', views.scrolling_game_level, name='scrolling-game-levels'),
    path('scrolling-game/end-session/', views.end_scrolling_game_session, name='end-scrolling-game-session'),

    # Instruments' urls
    path('instruments/', views.instruments_list, name='instruments-list'),
]