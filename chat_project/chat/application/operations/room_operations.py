from typing import Dict, Any
from ...domain import room, user
from ...utils import get_nested, set_value

def create_room_in_system(system_data: Dict[str, Any], room_name: str) -> Dict[str, Any]:
    """시스템에 채팅방 생성"""
    if not room_name:
        return system_data
    
    # 이미 존재하는 방인지 확인
    existing_room = get_nested(system_data, ["rooms", room_name])
    if existing_room is not None:
        return system_data
    
    # 새 방 생성
    new_room_data = room.create_room({}, room_name)
    return set_value(system_data, ["rooms", room_name], new_room_data)

def add_user_to_room(system_data: Dict[str, Any], room_name: str, user_id: str, channel_name: str) -> Dict[str, Any]:
    """시스템의 채팅방에 사용자 추가"""
    if not room_name or not user_id or not channel_name:
        return system_data
    
    # 방이 존재하는지 확인
    room_data = get_nested(system_data, ["rooms", room_name])
    if room_data is None:
        return system_data
    
    # 사용자 생성
    user_data = user.create_user({}, channel_name)
    
    # 방에 사용자 추가
    updated_room = room.add_user(room_data, user_id, user_data)
    return set_value(system_data, ["rooms", room_name], updated_room)

def remove_user_from_room(system_data: Dict[str, Any], room_name: str, user_id: str) -> Dict[str, Any]:
    """시스템의 채팅방에서 사용자 제거"""
    if not room_name or not user_id:
        return system_data
    
    # 방이 존재하는지 확인
    room_data = get_nested(system_data, ["rooms", room_name])
    if room_data is None:
        return system_data
    
    # 방에서 사용자 제거
    updated_room = room.remove_user(room_data, user_id)
    return set_value(system_data, ["rooms", room_name], updated_room) 