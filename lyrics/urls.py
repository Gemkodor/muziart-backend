from django.urls import path
from .views import *

urlpatterns = [
    path('', songs_list, name='songs-list'),
    path('create/', song_create, name='song-create'),
    path('<int:song_id>/', song_detail, name='song-detail'),
    path('<int:song_id>/update/', song_update, name='song-update'),
    path('<int:song_id>/delete/', song_delete, name='song-delete'),
    path('<int:song_id>/reset/', reset_progress, name='reset-progress'),
    path('<int:song_id>/complete-session/', complete_session, name='complete-session'),
]
