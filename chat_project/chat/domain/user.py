from typing import Dict, Any


def create_user(user_data: Dict[str, Any], channel_name: str) -> Dict[str, Any]:
    """사용자 데이터 구조 생성"""
    return {
        **user_data,
        "channelName": channel_name
    }