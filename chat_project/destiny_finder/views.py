from django.shortcuts import render
from django.http import JsonResponse
import json
from .domain import chat as chat_domain
from .domain import recommendation as recommendation_domain
from .application import llm_service
from .infrastructure import session_store

def chat(request):
    """운명 찾기 채팅 페이지"""
    return render(request, 'destiny_finder/chat.html')

def send_message(request):
    """LLM에게 메시지 전송 및 응답 받기"""
    if request.method == 'POST':
        body_data = json.loads(request.body)
        message = body_data.get('message', '')
        
        # 세션에서 채팅 정보 가져오기 또는 새로 생성
        chat_data = session_store.get_chat_from_session(request)
        
        # 사용자 메시지 추가 (불변성 유지)
        chat_data = chat_domain.add_message(chat_data, sender='user', content=message)
        
        # LLM 요청 생성
        chat_history = chat_domain.get_chat_history(chat_data)
        user_message = {'content': message}
        llm_request = llm_service.create_llm_request(user_message, chat_history)
        
        # LLM 응답 생성
        llm_response = llm_service.generate_llm_response(llm_request)
        
        # LLM 응답 추가
        chat_data = chat_domain.add_message(chat_data, sender='llm', content=llm_response["text"])
        
        # 세션에 채팅 정보 저장
        session_store.save_chat_to_session(request, chat_data)
        
        # 응답 준비
        response_data = {
            'response': llm_response["text"],
            'recommended_users': llm_response["recommended_users"]
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': '허용되지 않은 메서드'}, status=405)

def chat_history(request):
    """채팅 내역 반환"""
    chat_data = session_store.get_chat_from_session(request)
    messages = chat_domain.get_chat_history(chat_data)
    return JsonResponse({'messages': messages})

def get_recommendation_profile(request):
    if request.method == 'GET':
        try:
            # URL 파라미터에서 recommendation_id를 가져옵니다
            recommendation_id = request.GET.get('id')
            
            if not recommendation_id:
                return JsonResponse({'error': '사용자 ID가 필요합니다.'}, status=400)
                
            # 프로필 요청 데이터 생성
            profile_request = recommendation_domain.create_profile_request(recommendation_id)
                
            # ID를 사용하여 추천 프로필 가져오기
            profile = recommendation_domain.get_recommendation_profile(profile_request)
            
            if not profile:
                return JsonResponse({'error': '해당 ID의 사용자를 찾을 수 없습니다.'}, status=404)
                
            return JsonResponse(profile)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '허용되지 않는 메소드입니다.'}, status=405) 