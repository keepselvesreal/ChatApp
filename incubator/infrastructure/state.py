import copy
from typing import Dict, Any

from application.chat_management import ChatManagement
from infrastructure.consistency import ChatSystemConsistency


def diff_objects(data1, data2):
    """
    두 객체를 비교하여 다른 부분만 반환합니다.
    
    Args:
        data1: 첫 번째 비교 객체
        data2: 두 번째 비교 객체
        
    Returns:
        dict 또는 list: 두 객체 간의 차이를 담은 객체
    """
    # 빈 객체 생성 (data1이 리스트면 빈 리스트, 아니면 빈 딕셔너리)
    empty_object = [] if isinstance(data1, list) else {}
    
    # 두 객체가 같으면 빈 객체 반환
    if data1 == data2:
        return empty_object
    
    # 두 객체의 모든 키 합집합 구하기
    keys = set()
    if isinstance(data1, dict):
        keys.update(data1.keys())
    if isinstance(data2, dict):
        keys.update(data2.keys())
    elif isinstance(data1, list) and isinstance(data2, list):
        keys = set(range(max(len(data1), len(data2))))
    
    # 결과 객체 생성
    result = empty_object
    for k in keys:
        # 각 키에 대한 값 가져오기
        val1 = data1.get(k) if isinstance(data1, dict) else data1[k] if isinstance(data1, list) and k < len(data1) else None
        val2 = data2.get(k) if isinstance(data2, dict) else data2[k] if isinstance(data2, list) and k < len(data2) else None
        
        # 재귀적으로 비교
        res = diff(val1, val2)
        
        # 차이가 없으면 건너뛰기
        if (isinstance(res, (dict, list)) and not res) or res == "no-diff":
            continue
        
        # 결과 저장
        if isinstance(result, list):
            # 리스트인 경우 인덱스가 비어있을 수 있으므로 확장
            while len(result) <= k:
                result.append(None)
            result[k] = res
        else:
            # 딕셔너리인 경우 키에 값 설정
            result[k] = res
    
    return result


def diff(data1, data2):
    """
    두 데이터를 비교하여 차이점을 반환합니다.
    
    Args:
        data1: 첫 번째 비교 데이터
        data2: 두 번째 비교 데이터
        
    Returns:
        다른 경우 data2를, 같은 경우 "no-diff"를, 객체인 경우 차이점 객체를 반환
    """
    # 둘 다 객체(리스트 또는 딕셔너리)인 경우 재귀 호출
    if isinstance(data1, (dict, list)) and isinstance(data2, (dict, list)):
        return diff_objects(data1, data2)
    
    # 값이 다르면 data2 반환
    if data1 != data2:
        return data2
    
    # 값이 같으면 "no-diff" 반환
    return "no-diff"


def information_paths(obj, path=None):
    """
    객체의 모든 리프 노드까지의 경로를 배열로 반환합니다.
    
    Args:
        obj: 경로를 찾을 객체(딕셔너리)
        path: 현재까지의 경로(기본값: None)
        
    Returns:
        list: 모든 리프 노드까지의 경로 목록
    """
    if path is None:
        path = []
    
    result = []
    
    # 딕셔너리의 모든 키-값 쌍을 순회
    for key, value in obj.items():
        current_path = path + [key]
        
        # 값이 딕셔너리인 경우 재귀적으로 탐색
        if isinstance(value, dict):
            result.extend(information_paths(value, current_path))
        else:
            # 리프 노드인 경우 현재 경로 추가
            result.append(current_path)
    
    return result


def have_path_in_common(diff1, diff2):
    """
    두 객체 간에 공통된 경로가 있는지 확인합니다.
    
    Args:
        diff1: 첫 번째 비교 객체
        diff2: 두 번째 비교 객체
        
    Returns:
        bool: 공통 경로가 있으면 True, 없으면 False
    """
    # 각 객체의 모든 경로 수집
    paths1 = information_paths(diff1)
    paths2 = information_paths(diff2)
    
    # 공통 경로 찾기
    common_paths = set()
    for path1 in paths1:
        path1_tuple = tuple(path1)  # 리스트는 해시 불가능하므로 튜플로 변환
        for path2 in paths2:
            path2_tuple = tuple(path2)
            if path1_tuple == path2_tuple:
                common_paths.add(path1_tuple)
                break
    
    # 공통 경로가 있는지 여부 반환
    return len(common_paths) > 0


def merge(target, source):
    """
    두 객체를 깊은 수준까지 병합합니다. (lodash의 _.merge 함수와 유사)
    
    Args:
        target: 병합할 대상 객체
        source: 병합의 출처가 되는 객체
    
    Returns:
        dict: 병합된 객체
    """
    # source가 None이거나 딕셔너리가 아니면 target 반환
    if source is None or not isinstance(source, dict):
        return target
    
    # target이 None이거나 딕셔너리가 아니면 source의 복사본 반환
    if target is None or not isinstance(target, dict):
        return dict(source)
    
    result = dict(target)  # target의 복사본 생성
    
    # source의 모든 키를 순회
    for key, value in source.items():
        # 두 객체 모두 같은 키에 딕셔너리를 가지고 있다면 재귀적으로 병합
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge(result[key], value)
        else:
            # 그렇지 않으면 source의 값으로 덮어쓰기
            result[key] = value
            
    return result


class SystemConsistency:
    """시스템 일관성 클래스."""

    @staticmethod
    def three_way_merge(current: Any, previous: Any, next_state: Any) -> Any:
        """3방향 병합을 수행합니다."""
        previous_to_current = diff(previous, current)
        previous_to_next = diff(previous, next_state)
        if have_path_in_common(previous_to_current, previous_to_next):
            merged = copy.deepcopy(current)
            return merge(merged, previous_to_next)
        raise ValueError("Conflicting concurrent mutations.")

    @staticmethod
    def reconcile(current: Any, previous: Any, next_state: Any) -> Any:
        """상태를 조정합니다."""
        if current == previous:
            return next_state
        return SystemConsistency.three_way_merge(current, previous, next_state)


class ChatSystemState:
    """시스템 상태 클래스."""

    _system_data: Dict[str, Any] = {}  # 클래스 변수. 외부에서 직접 접근하지 않도록 _로 시작

    @classmethod
    def get(cls) -> Any:
        """현재 시스템 데이터를 반환합니다."""
        return cls._system_data

    @classmethod
    def set(cls, system_data: Any):
        """시스템 데이터를 설정합니다."""
        cls._system_data = system_data

    @classmethod
    def commit(cls, previous: Any, next_state: Any):
        """시스템 데이터를 커밋합니다."""
        next_system_data = SystemConsistency.reconcile(
            ChatSystemState.get(),
            previous,
            next_state
        )
        # SystemValidity 파일 만든 후 validate 함수 만들고, schema 이용해 유효성 검증하게 할 듯
        # if not SystemValidity.validate(previous, next_system_data):
        #     raise ValueError("The system data to be committed is not valid!")
        ChatSystemState.set(next_system_data) 