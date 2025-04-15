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

def validate_chat_message(data: Dict[str, Any]) -> bool:
    """채팅 메시지 데이터 스키마 검증"""
    return validate(data, "message_schema")
