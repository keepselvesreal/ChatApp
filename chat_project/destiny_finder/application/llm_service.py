from typing import Dict, List, Any
import random
from datetime import datetime
from ..domain import recommendation as recommendation_domain

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

def generate_llm_response(message: str, chat_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """사용자 메시지와 대화 내역을 바탕으로 LLM 응답 생성"""
    # 추천 사용자 목록 가져오기
    recommended_users = recommendation_domain.get_recommendations(message)
    
    # 추천 사용자 목록을 HTML 형식으로 포맷팅 (클릭 가능한 링크)
    user_mentions = ", ".join([f"<a href='#' class='user-mention' data-user-id='{user['id']}'>{user['name']}</a>" for user in recommended_users])
    
    # 응답 메시지 생성
    response_text = f"당신에게 맞는 사람을 찾아봤어요. {user_mentions} 중에서 마음에 드는 분이 있으신가요? 이름을 클릭하면 더 자세한 정보를 볼 수 있어요."
    
    return {
        "text": response_text,
        "recommended_users": recommended_users
    } 