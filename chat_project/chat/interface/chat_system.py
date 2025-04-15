from typing import Dict, Any

from ..application.chat_management import ChatManagement
from ..application.validation.schema_validator import validate_chat_message
from ..infrastructure.state import ChatSystemState


class ChatSystem:
    """채팅 시스템 작업을 수행하는 클래스"""
    
    @staticmethod
    async def handle_connection(connection_data: Dict[str, Any], channel_layer):
        """새 연결 처리"""
        await ChatSystem.create_room(connection_data)
        await ChatSystem.add_user(connection_data)
        await ChatSystem.send_join_message(connection_data, channel_layer)
    
    @staticmethod
    async def handle_disconnection(connection_data: Dict[str, Any], channel_layer):
        """연결 종료 처리"""
        await ChatSystem.remove_user(connection_data)
        await ChatSystem.send_leave_message(connection_data, channel_layer)
    
    @staticmethod
    async def handle_message(connection_data: Dict[str, Any], content: str, channel_layer):
        """메시지 수신 처리"""
        message = ChatManagement.create_user_message(connection_data, content)
        if not validate_chat_message(message):
            raise ValueError("Invalid message format")
        
        await channel_layer.group_send(
            connection_data["roomGroupName"],
            message
        )
    
    @staticmethod
    async def create_room(connection_data: Dict[str, Any]):
        """채팅방 생성"""
        previous = ChatSystemState.get()
        next_state = ChatManagement.create_room(previous, connection_data)
        ChatSystemState.commit(previous, next_state)
    
    @staticmethod
    async def add_user(connection_data: Dict[str, Any]):
        """채팅방에 사용자 추가"""
        previous = ChatSystemState.get()
        next_state = ChatManagement.add_user_to_room(previous, connection_data)
        ChatSystemState.commit(previous, next_state)
    
    @staticmethod
    async def remove_user(connection_data: Dict[str, Any]):
        """채팅방에서 사용자 제거"""
        previous = ChatSystemState.get()
        next_state = ChatManagement.remove_user_from_room(previous, connection_data)
        ChatSystemState.commit(previous, next_state)
    
    @staticmethod
    async def send_join_message(connection_data: Dict[str, Any], channel_layer):
        """입장 메시지 전송"""
        join_message = ChatManagement.create_join_message(connection_data)
        await channel_layer.group_send(
            connection_data["roomGroupName"],
            join_message
        )
    
    @staticmethod
    async def send_leave_message(connection_data: Dict[str, Any], channel_layer):
        """퇴장 메시지 전송"""
        leave_message = ChatManagement.create_leave_message(connection_data)
        await channel_layer.group_send(
            connection_data["roomGroupName"],
            leave_message
        )