from typing import Dict, Any, List

def get_nested(data: Dict[str, Any], path: List[str], default=None) -> Any:
    """중첩된 딕셔너리에서 값 가져오기"""
    current = data
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def set_value(data: Dict[str, Any], path: List[str], value: Any) -> Dict[str, Any]:
    """중첩된 딕셔너리에 값 설정하기"""
    if not path:
        return value
    
    result = data.copy()
    current = result
    
    # 마지막 키를 제외한 모든 키에 대해 중첩 딕셔너리 탐색
    for i, key in enumerate(path[:-1]):
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    
    # 마지막 키에 값 설정
    current[path[-1]] = value
    return result