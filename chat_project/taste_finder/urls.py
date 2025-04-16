from django.urls import path
from . import views

app_name = 'taste_finder'

urlpatterns = [
    path('question/', views.question_view, name='question'),
    path('question/thanks/', views.question_thanks, name='question_thanks'),
] 