from typing import Dict, Any

from ..domain import room, user, message
from ..utils.helper import get_nested, set_value 


class ChatManagement:
    """채팅 시스템 데이터 처리를 위한 클래스"""
    
    @staticmethod
    def create_initial_system_data() -> Dict[str, Any]:
        """초기 시스템 데이터 생성"""
        return {
            "rooms": {}
        }
    
    @staticmethod
    def create_room(system_data: Dict[str, Any], connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """시스템에 채팅방 생성"""
        room_name = connection_data.get("roomName", "")
        new_room = room.create_room({}, room_name)
        return set_value(system_data, ["rooms", room_name], new_room)
    
    @staticmethod
    def add_user_to_room(system_data: Dict[str, Any], connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """채팅방에 사용자 추가"""
        room_name = connection_data.get("roomName", "")
        user_id = connection_data.get("userId", "")
        channel_name = connection_data.get("channelName", "")
        
        user_data = user.create_user({}, channel_name)
        return set_value(system_data, ["rooms", room_name, "users", user_id], user_data)
    
    @staticmethod
    def remove_user_from_room(system_data: Dict[str, Any], connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """채팅방에서 사용자 제거"""
        room_name = connection_data["roomGroupName"]
        user_id = connection_data["userId"]
        
        # 방이 존재하는지 확인
        room_data = get_nested(system_data, ["rooms", room_name])
        if room_data is None:
            return system_data
        
        # 방에서 사용자 제거
        updated_room = room.remove_user(room_data, user_id)
        return set_value(system_data, ["rooms", room_name], updated_room)
    
    @staticmethod
    def create_join_message(connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 입장 메시지 생성"""
        user_id = connection_data.get("userId", "")
        return message.create_message(
            {},
            "chat_message",
            f'{user_id}님이 입장했습니다.',
            "system"
        )
    
    @staticmethod
    def create_leave_message(connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 퇴장 메시지 생성"""
        user_id = connection_data.get("userId", "")
        return message.create_message(
            {},
            "chat_message",
            f'{user_id}님이 퇴장했습니다.',
            "system"
        )
    
    @staticmethod
    def create_system_message(content: str) -> Dict[str, Any]:
        return message.create_message({}, "chat_message", content, "system")
    
    @staticmethod
    def create_user_message(connection_data: Dict[str, Any], content: str) -> Dict[str, Any]:
        """사용자 채팅 메시지 생성"""
        user_id = connection_data.get("userId", "")
        return message.create_message({}, "chat_message", content, user_id)