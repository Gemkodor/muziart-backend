from django.urls import path
from . import views

urlpatterns = [
    path('', views.quests_list, name='quests_list'),
    path('<int:quest_id>/claim/', views.claim_quest, name='claim_quest'),
]
