from typing import Dict, Any


def create_user(channel_name: str) -> Dict[str, Any]:
    """사용자 데이터 구조 생성"""
    return {
        "channelName": channel_name
    }