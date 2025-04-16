from typing import Dict, Any, Tuple, List
from ...application.operations import room_operations, message_operations
from ...application.validation import schema_validator
import base64

def _encode_group_name(room_name: str) -> str:
    """방 이름을 안전한 그룹 이름으로 인코딩"""
    return base64.urlsafe_b64encode(room_name.encode()).decode()

def handle_connection_flow(connection_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Tuple]]:
    """연결 처리 흐름"""
    if not schema_validator.validate_connection_data(connection_data):
        return {}, [("error", "Invalid connection data")]
    
    room_name = connection_data["roomName"]
    user_id = connection_data["userId"]
    channel_name = connection_data["channelName"]
    room_group_name = f"chat_{_encode_group_name(room_name)}"
    
    # 방 생성
    system_data = room_operations.create_room_in_system({}, room_name)
    
    # 사용자 추가
    system_data = room_operations.add_user_to_room(system_data, room_name, user_id, channel_name)
    
    # 입장 메시지 생성
    join_message = message_operations.create_system_join_message(user_id)
    
    # 효과 정의
    effects = [
        ("group_add", room_group_name, channel_name),
        ("group_send", room_group_name, join_message)
    ]
    
    return system_data, effects

def handle_disconnection_flow(connection_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Tuple]]:
    """연결 종료 처리 흐름"""
    if not schema_validator.validate_connection_data(connection_data):
        return {}, [("error", "Invalid connection data")]
    
    room_name = connection_data["roomName"]
    user_id = connection_data["userId"]
    channel_name = connection_data["channelName"]
    room_group_name = f"chat_{_encode_group_name(room_name)}"
    
    # 사용자 제거
    system_data = room_operations.remove_user_from_room({}, room_name, user_id)
    
    # 퇴장 메시지 생성
    leave_message = message_operations.create_system_leave_message(user_id)
    
    # 효과 정의
    effects = [
        ("group_send", room_group_name, leave_message),
        ("group_discard", room_group_name, channel_name)
    ]
    
    return system_data, effects

def handle_message_flow(connection_data: Dict[str, Any], content: str) -> Tuple[Dict[str, Any], List[Tuple]]:
    """메시지 처리 흐름"""
    if not schema_validator.validate_connection_data(connection_data) or not content:
        return {}, [("error", "Invalid message data")]
    
    user_id = connection_data["userId"]
    room_name = connection_data["roomName"]
    room_group_name = f"chat_{_encode_group_name(room_name)}"
    
    # 메시지 생성
    message_data = message_operations.create_user_message(content, user_id)
    
    # 메시지 검증
    if not schema_validator.validate_chat_message(message_data):
        error_message = message_operations.create_error_message("메시지 형식이 올바르지 않습니다.")
        return {}, [("send", connection_data["channelName"], error_message)]
    
    # 효과 정의
    effects = [
        ("group_send", room_group_name, message_data)
    ]
    
    return {}, effects 