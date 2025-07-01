from django.urls import path
from . import views

urlpatterns = [
    path("deezer/albums/<str:album_id>/", views.get_deezer_album, name="deezer-album-tracks"),
]