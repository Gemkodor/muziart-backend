from django.urls import path
from . import views

urlpatterns = [
    path("blind-test/tracks/random/<int:nb_questions>/", views.random_track, name="random-track"),
]