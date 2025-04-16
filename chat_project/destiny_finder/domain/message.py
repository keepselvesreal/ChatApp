from typing import Dict, Any, Optional
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

def get_message_content(message: Dict[str, Any]) -> str:
    """메시지 내용 반환"""
    return message.get("content", "")

def get_message_timestamp(message: Dict[str, Any]) -> Any:
    """메시지 타임스탬프 반환"""
    return message.get("timestamp", 0)

def get_message_sender(message: Dict[str, Any]) -> str:
    """메시지 발신자 반환"""
    return message.get("sender", "") 