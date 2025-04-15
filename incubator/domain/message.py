from typing import Dict, Any


def create_message(message_type: str, content: str, user_id: str) -> Dict[str, Any]:
        """메시지 데이터 구조 생성"""
        return {
            "type": message_type,
            "message": content,
            "userId": user_id
        }