from typing import Dict, Any
from ...domain import message

def create_user_message(content: str, user_id: str) -> Dict[str, Any]:
    """사용자가 보낸 채팅 메시지 생성"""
    return message.create_message({}, "chat_message", content, user_id)

def create_system_join_message(user_id: str) -> Dict[str, Any]:
    """사용자 입장 시스템 메시지 생성"""
    return message.create_message(
        {},
        "system_message",
        f"{user_id}님이 입장했습니다.",
        "system"
    )

def create_system_leave_message(user_id: str) -> Dict[str, Any]:
    """사용자 퇴장 시스템 메시지 생성"""
    return message.create_message(
        {},
        "system_message",
        f"{user_id}님이 퇴장했습니다.",
        "system"
    )

def create_error_message(error_content: str) -> Dict[str, Any]:
    """오류 메시지 생성"""
    return message.create_message(
        {},
        "error_message",
        error_content,
        "system"
    ) 