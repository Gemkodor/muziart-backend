from django.urls import path
from . import views

urlpatterns = [
    # Blind test's urls
    path("blind-test/tracks/random/<int:nb_questions>/", views.random_track, name="random-track"),
    path("blind-test/complete/", views.complete_blind_test, name="complete-blind-test"),
    
    # Scrolling game's urls
    path('scrolling-game/level/<str:clef>/<int:level_number>/', views.scrolling_game_level, name='scrolling-game-levels'),

    # Generic game progression
    path('progression/end-session/', views.end_game_progression_session, name='end-game-progression-session'),

    # Instruments' urls
    path('instruments/', views.instruments_list, name='instruments-list'),
    path('instruments/categories/', views.instruments_categories, name='instruments-categories'),
]