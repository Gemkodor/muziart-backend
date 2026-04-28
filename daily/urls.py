from django.urls import path
from . import views

urlpatterns = [
    path('today/', views.today_program, name='daily_today'),
    path('activities/<int:activity_id>/complete/', views.complete_activity, name='daily_complete_activity'),
    path('extra/', views.add_extra_activity, name='daily_extra'),
]
