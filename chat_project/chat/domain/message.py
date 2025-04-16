from typing import Dict, Any
from ..utils import get_current_timestamp


def create_message(message_data: Dict[str, Any], message_type: str, content: str, sender_id: str) -> Dict[str, Any]:
    """새로운 메시지 데이터 생성"""
    return {
        "type": message_type,
        "content": content,
        "sender_id": sender_id,
        "timestamp": get_current_timestamp()
    }