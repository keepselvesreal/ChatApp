from typing import Dict, Any
import copy

from ..utils.helper import set_value


def create_room(room_data: Dict[str, Any], room_name: str) -> Dict[str, Any]:
        """채팅방 데이터 구조 생성"""
        return {
            **room_data,
            "roomName": room_name,
            "users": {}
        }
    

def add_user(room_data: Dict[str, Any], user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """채팅방에 사용자 추가"""
    return set_value(room_data, ["users", user_id], user_data)


def remove_user(room_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """채팅방에서 사용자 제거"""
    new_room_data = copy.deepcopy(room_data)
    if user_id in new_room_data["users"]:
        del new_room_data["users"][user_id]
    return new_room_data