class ChatSystemConsistency:
    """시스템 일관성 관리 클래스"""
    
    @staticmethod
    def reconcile(current: Dict[str, Any], previous: Dict[str, Any], next_state: Dict[str, Any]) -> Dict[str, Any]:
        """상태를 조정"""
        if current == previous:
            return next_state
        # 실제 구현에서는 three_way_merge 등의 복잡한 로직이 들어갈 수 있음
        return next_state  