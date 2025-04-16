from typing import Dict, Any
from ..utils import get_current_timestamp


def create_user(user_data: Dict[str, Any], channel_name: str) -> Dict[str, Any]:
    """새로운 사용자 데이터 생성"""
    return {
        "channel_name": channel_name,
        "joined_at": get_current_timestamp(),
        "last_activity": get_current_timestamp()
    }

def update_activity(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """사용자 활동 시간 업데이트"""
    return {
        **user_data,
        "last_activity": get_current_timestamp()
    }