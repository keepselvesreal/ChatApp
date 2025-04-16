import json
import jsonschema
from pathlib import Path
from typing import Any, Dict

def _load_schema(name: str) -> Dict[str, Any]:
    schema_path = Path(__file__).parent.parent.parent / "domain" / "schema" / f"{name}.json"
    with open(schema_path) as f:
        return json.load(f)

def validate(data: Dict[str, Any], schema_name: str) -> bool:
    """일반적인 데이터 검증 함수"""
    try:
        schema = _load_schema(schema_name)
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False

def validate_chat_system(data: Dict[str, Any]) -> bool:
    """채팅 시스템 전체 데이터 스키마 검증"""
    return validate(data, "chat_system_schema")

def validate_chat_message(message_data: Dict[str, Any]) -> bool:
    """채팅 메시지 검증"""
    required_fields = ["type", "content", "sender_id", "timestamp"]
    return all(field in message_data for field in required_fields) and message_data["content"]

def validate_connection_data(connection_data: Dict[str, Any]) -> bool:
    """연결 데이터 검증"""
    required_fields = ["roomName", "userId", "channelName"]
    return all(field in connection_data for field in required_fields)

def validate_room_name(room_name: str) -> bool:
    """방 이름 검증"""
    return isinstance(room_name, str) and len(room_name) > 0 and len(room_name) <= 50
