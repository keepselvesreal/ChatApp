from django.urls import path
from . import views

app_name = 'chat'  # 앱 네임스페이스 추가

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('question/', views.question, name='question'),  # 리다이렉트용으로 유지
    path('fortune/', views.fortune, name='fortune'),
]