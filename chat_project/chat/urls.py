from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('question/', views.question, name='question'),
    path('fortune/', views.fortune, name='fortune'),
]