from django.shortcuts import render
from django.http import JsonResponse
import json
from .domain import chat as chat_domain
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
        
        # LLM 응답 생성
        chat_history = chat_domain.get_chat_history(chat_data)
        llm_response = llm_service.generate_llm_response(message, chat_history)
        
        # LLM 응답 추가
        chat_data = chat_domain.add_message(chat_data, sender='llm', content=llm_response)
        
        # 세션에 채팅 정보 저장
        session_store.save_chat_to_session(request, chat_data)
        
        return JsonResponse({'response': llm_response})
    
    return JsonResponse({'error': '허용되지 않은 메서드'}, status=405)

def chat_history(request):
    """채팅 내역 반환"""
    chat_data = session_store.get_chat_from_session(request)
    messages = chat_domain.get_chat_history(chat_data)
    return JsonResponse({'messages': messages}) 