from django.urls import path
from . import views

app_name = 'destiny_finder'

urlpatterns = [
    path('', views.chat, name='chat'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/chat-history/', views.chat_history, name='chat_history'),
    path('api/recommendation-profile/<str:recommendation_id>/', views.get_recommendation_profile, name='get_recommendation_profile'),
] 