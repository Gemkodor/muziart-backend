from django.urls import path
from . import views

urlpatterns = [
    path("deezer/albums/<str:album_id>/", views.deezer_albums, name="album-detail"),
]