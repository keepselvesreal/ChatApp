from django.db import models
from django.utils import timezone

# Create your models here.

class UserAnswer(models.Model):
    question_id = models.CharField(max_length=100)  # 질문 식별자
    question_text = models.CharField(max_length=500)  # 질문 내용
    answer_text = models.TextField()  # 사용자 답변
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    user_id = models.CharField(max_length=100, blank=True, null=True)  # 사용자 식별자
    
    def __str__(self):
        return f"Answer to: {self.question_text[:30]}"
