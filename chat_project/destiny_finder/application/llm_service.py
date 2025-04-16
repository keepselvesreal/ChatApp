from typing import Dict, List, Any
import random
from datetime import datetime

def get_mock_llm_responses() -> List[str]:
    """가상 LLM 응답 목록"""
    return [
        "당신에게는 창의적이고 예술적인 성향을 가진 파트너가 잘 어울릴 것 같네요.",
        "안정적이고 신뢰할 수 있는 성격의 파트너를 찾아보세요.",
        "당신의 활발한 에너지를 함께 나눌 수 있는 외향적인 사람이 좋을 것 같아요.",
        "깊이 있는 대화가 가능한 지적인 파트너가 당신을 행복하게 할 수 있을 거예요.",
        "당신의 가치관을 존중하고 유사한 목표를 가진 사람을 만나면 좋은 관계가 될 것 같아요."
    ]

def get_mock_llm_follow_ups() -> List[str]:
    """가상 LLM 후속 질문 목록"""
    return [
        "어떤 성격의 사람을 만나고 싶으신가요?",
        "평소 어떤 가치관을 중요하게 생각하시나요?",
        "미래 파트너에게 가장 중요하게 생각하는 특성은 무엇인가요?",
        "이전 관계에서 배운 점이 있다면 무엇인가요?"
    ]

def generate_llm_response(message: str, chat_history: List[Dict[str, Any]]) -> str:
    """사용자 메시지와 대화 내역을 바탕으로 LLM 응답 생성"""
    responses = get_mock_llm_responses()
    follow_ups = get_mock_llm_follow_ups()
    
    # 간단한 응답 선택 (실제 구현에서는 더 복잡한 로직이 필요)
    response = random.choice(responses)
    
    # 50% 확률로 후속 질문 추가
    if random.random() > 0.5:
        response += "\n\n" + random.choice(follow_ups)
    
    return response 