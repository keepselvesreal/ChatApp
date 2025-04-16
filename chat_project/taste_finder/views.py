from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import logging

from .domain.question_service import get_active_question, save_user_answer

# 로그 설정
logger = logging.getLogger(__name__)

def question_view(request):
    """오늘의 질문 페이지 뷰 함수"""
    logger.error(f"요청 방식: {request.method}, PATH: {request.path}")
    
    # 세션 설정이 없는 경우 세션 시작
    if not request.session.session_key:
        request.session.create()
        logger.error(f"세션 생성: {request.session.session_key}")
    
    # 오늘의 질문 가져오기 (도메인 서비스 사용)
    question_data = get_active_question()
    
    if request.method == 'POST':
        logger.error(f"POST 데이터: {request.POST}")
        answer_text = request.POST.get('answer_text')
        logger.error(f"답변 텍스트: {answer_text}")
        
        if answer_text:
            # 사용자 ID - 실제로는 인증 시스템에서 가져오거나 세션 ID 활용
            user_id = request.session.session_key or 'anonymous'
            logger.error(f"사용자 ID: {user_id}")
            
            # 답변 데이터 구성
            answer_data = {
                'question_id': question_data['id'],
                'question_text': question_data['question_text'],
                'answer_text': answer_text,
                'user_id': user_id
            }
            
            try:
                # 답변 저장 (도메인 서비스 사용)
                save_user_answer(answer_data)
                logger.error("답변 저장 성공")
                return redirect('/taste/question/thanks/')
            except Exception as e:
                logger.error(f"답변 저장 오류: {e}")
                return HttpResponse(f"오류가 발생했습니다: {e}", status=500)
        else:
            logger.error("답변 텍스트가 없음")
    
    return render(request, 'taste_finder/question.html', {'question': question_data})

def question_thanks(request):
    """질문 답변 감사 페이지 뷰 함수"""
    return render(request, 'taste_finder/thanks.html')
