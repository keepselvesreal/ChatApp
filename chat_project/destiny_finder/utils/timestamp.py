from datetime import datetime

def get_current_timestamp() -> str:
    """현재 시간의 ISO 형식 문자열 반환"""
    return datetime.now().isoformat() 