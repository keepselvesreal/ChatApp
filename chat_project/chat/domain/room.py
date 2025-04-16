from typing import Dict, Any, Optional
from dataclasses import dataclass
import copy

from ..utils import get_current_timestamp


@dataclass
class Room:
    """채팅방 도메인 클래스"""
    room_name: str
    users: Dict[str, Any]
    
    @classmethod
    def create(cls, room_name: str) -> 'Room':
        """새로운 채팅방 생성"""
        return cls(
            room_name=room_name,
            users={}
        )
    
    def add_user(self, user_id: str, user_data: Dict[str, Any]) -> 'Room':
        """채팅방에 사용자 추가"""
        self.users[user_id] = user_data
        return self
    
    def remove_user(self, user_id: str) -> 'Room':
        """채팅방에서 사용자 제거"""
        if user_id in self.users:
            del self.users[user_id]
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Room 객체를 딕셔너리로 변환"""
        return {
            "roomName": self.room_name,
            "users": self.users
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Room':
        """딕셔너리에서 Room 객체 생성"""
        return cls(
            room_name=data.get("roomName", ""),
            users=data.get("users", {})
        )


def create_room(room_data: Dict[str, Any], room_name: str) -> Dict[str, Any]:
    """새로운 채팅방 데이터 생성"""
    return {
        "name": room_name,
        "users": {},
        "created_at": get_current_timestamp()
    }


def add_user(room_data: Dict[str, Any], user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """채팅방에 사용자 추가"""
    return {
        **room_data,
        "users": {
            **room_data.get("users", {}),
            user_id: user_data
        }
    }


def remove_user(room_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """채팅방에서 사용자 제거"""
    if user_id not in room_data.get("users", {}):
        return room_data
    
    # 사용자 목록에서 제거한 새 맵 생성
    new_users = {k: v for k, v in room_data.get("users", {}).items() if k != user_id}
    
    return {
        **room_data,
        "users": new_users
    }


def get_users(room_data: Dict[str, Any]) -> Dict[str, Any]:
    """채팅방의 모든 사용자 반환"""
    return room_data.get("users", {})