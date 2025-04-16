from typing import Dict, Any
import copy
from ..utils.timestamp import get_current_timestamp

def create_message(sender: str, content: str) -> Dict[str, Any]:
    """새로운 메시지 데이터 생성"""
    return {
        "sender": sender,
        "content": content,
        "timestamp": get_current_timestamp()
    }

def is_user_message(message: Dict[str, Any]) -> bool:
    """사용자가 보낸 메시지인지 확인"""
    return message.get("sender") == "user"

def is_llm_message(message: Dict[str, Any]) -> bool:
    """LLM이 보낸 메시지인지 확인"""
    return message.get("sender") == "llm" 