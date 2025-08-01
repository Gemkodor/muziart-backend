from django.urls import path
from . import views_auth, views_collections, views_keys, views_lessons

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
    
    # Collections endpoints
    path('api/collections/cards/', views_collections.get_cards, name='get_cards'),
    path('api/collections/cards/unlock', views_collections.unlock_card, name='unlock_card'),
    
    path('api/lessons/', views_lessons.lessons_list, name='lessons-list'),
    
    # Index endpoint
    path('', views_auth.index, name='index'),
]