from django.urls import path
from . import views_auth, views_keys, views_games

urlpatterns = [
    # Authentication endpoints
    path('api/set-csrf-token', views_auth.set_csrf_token, name='set_csrf_token'),
    path('api/login', views_auth.login_view, name='login'),
    path('api/logout', views_auth.logout_view, name='logout'),
    path('api/user', views_auth.user, name='user'),
    path('api/register', views_auth.register, name='register'),
    
    # Keys endpoints
    path('api/keys/add_keys/', views_keys.add_keys, name='add_keys'),
    path('api/keys/add_xp/', views_keys.add_xp, name='add_xp'),
    
    # Instruments
    path('api/instruments/', views_games.instruments_list, name='instruments-list'),
    
    path('api/scrolling-game/level/<int:level_number>/', views_games.scrolling_game_level, name='scrolling-game-levels'),
    
    # Index endpoint
    path('', views_auth.index, name='index'),
]