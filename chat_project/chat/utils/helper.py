from typing import Dict, Any, List
import copy

def get_nested(data: Dict[str, Any], path: List[str], default=None) -> Any:
    """중첩된 딕셔너리에서 값을 안전하게, Lodash _.get 방식으로 가져오는 함수"""
    current = data
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def set_value(data: Dict[str, Any], path, value) -> Dict[str, Any]:
    """불변 방식으로 중첩된 딕셔너리에 값을 설정하는 함수"""
    if isinstance(path, str):
        path = [path]
    
    result = copy.deepcopy(data)
    current = result
    
    # 마지막 키를 제외한 모든 키로 경로 탐색
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # 마지막 키에 값 설정
    current[path[-1]] = value
    return result