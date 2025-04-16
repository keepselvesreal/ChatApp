from django.utils import timezone
import random
import logging

# 로그 설정
logger = logging.getLogger(__name__)

def get_active_question():
    """오늘의 질문을 반환하는 함수"""
    # 직접 흥미로운 질문들을 정의
    questions = [
        {
            'id': 'life_value',
            'question_text': '당신의 인생에서 가장 중요한 가치는 무엇인가요?'
        },
        {
            'id': 'hobby',
            'question_text': '여가 시간에 가장 즐겨하는 활동은 무엇인가요?'
        },
        {
            'id': 'dream',
            'question_text': '어린 시절 꿈꿨던 직업은 무엇이었나요?'
        },
        {
            'id': 'travel',
            'question_text': '가장 인상 깊었던 여행지는 어디인가요?'
        },
        {
            'id': 'food',
            'question_text': '당신의 취향을 가장 잘 드러내는 음식은 무엇인가요?'
        }
    ]
    
    # 랜덤하게 질문 선택
    selected_question = random.choice(questions)
    
    # 현재 시간 추가
    selected_question['created_at'] = timezone.now()
    
    return selected_question

def save_user_answer(answer_data):
    """사용자 답변을 저장하는 함수"""
    from ..models import UserAnswer
    
    logger.error(f"저장 시도 데이터: {answer_data}")
    
    try:
        # 사용자 답변 직접 저장 (DOP - 간단한 함수형 접근)
        answer = UserAnswer(
            question_id=answer_data['question_id'],
            question_text=answer_data['question_text'],
            answer_text=answer_data['answer_text'],
            user_id=answer_data.get('user_id', 'anonymous')  # 기본값 설정
        )
        logger.error(f"UserAnswer 객체 생성: {answer}")
        answer.save()
        logger.error("UserAnswer 저장 완료")
        
        # 저장된 데이터를 딕셔너리로 반환 (DOP 원칙)
        result = {
            'id': answer.id,
            'question_id': answer.question_id,
            'question_text': answer.question_text,
            'answer_text': answer.answer_text,
            'user_id': answer.user_id,
            'created_at': answer.created_at
        }
        logger.error(f"반환 결과: {result}")
        return result
    except Exception as e:
        logger.error(f"답변 저장 중 오류 발생: {str(e)}")
        raise 