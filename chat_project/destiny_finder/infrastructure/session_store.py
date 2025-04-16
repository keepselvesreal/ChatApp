from typing import Dict, Any, Optional
from django.http import HttpRequest
from ..domain import chat as chat_domain

def get_chat_from_session(request: HttpRequest) -> Dict[str, Any]:
    """세션에서 채팅 데이터 가져오기, 없으면 새로 생성"""
    if 'destiny_chat' not in request.session:
        return chat_domain.create_chat(session_id=request.session.session_key or 'anonymous')
    return request.session['destiny_chat']

def save_chat_to_session(request: HttpRequest, chat_data: Dict[str, Any]) -> None:
    """채팅 데이터를 세션에 저장"""
    request.session['destiny_chat'] = chat_data
    request.session.modified = True 