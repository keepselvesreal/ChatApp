from typing import Dict, List, Any
import copy
from ..utils.timestamp import get_current_timestamp
from .message import create_message

def create_chat(session_id: str) -> Dict[str, Any]:
    """새로운 채팅 데이터 생성"""
    return {
        "session_id": session_id,
        "messages": [],
        "created_at": get_current_timestamp()
    }

def add_message(chat_data: Dict[str, Any], sender: str, content: str) -> Dict[str, Any]:
    """새 메시지 추가하고 새 채팅 객체 반환 (불변성 유지)"""
    new_chat = copy.deepcopy(chat_data)
    message = create_message(sender, content)
    new_chat["messages"].append(message)
    return new_chat

def get_chat_history(chat_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """채팅 내역 반환"""
    return chat_data.get("messages", []) 