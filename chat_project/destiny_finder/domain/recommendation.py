from typing import Dict, List, Any
import random
from ..utils.timestamp import get_current_timestamp

def get_mock_recommendations() -> List[Dict[str, Any]]:
    """가상 추천 사용자 데이터 목록 반환"""
    return [
        {
            "id": "user1",
            "name": "김지민",
            "age": 28,
            "gender": "여성",
            "interests": ["여행", "독서", "영화감상"],
            "profile_text": "안녕하세요, 저는 김지민입니다. 여행을 좋아하고 새로운 사람들과의 만남을 즐기는 편입니다."
        },
        {
            "id": "user2",
            "name": "이준호",
            "age": 32,
            "gender": "남성",
            "interests": ["음악", "요리", "등산"],
            "profile_text": "안녕하세요, 저는 이준호입니다. 음악과 요리를 좋아하며 주말에는 종종 산에 오릅니다."
        },
        {
            "id": "user3",
            "name": "박소연",
            "age": 25,
            "gender": "여성",
            "interests": ["그림", "사진", "댄스"],
            "profile_text": "안녕하세요, 박소연입니다. 그림 그리기와 사진 찍기를 좋아하고 취미로 댄스를 배우고 있습니다."
        },
        {
            "id": "user4",
            "name": "최민준",
            "age": 30,
            "gender": "남성",
            "interests": ["게임", "프로그래밍", "테니스"],
            "profile_text": "안녕하세요, 최민준입니다. 개발자로 일하고 있으며 취미로 게임과 테니스를 즐깁니다."
        },
        {
            "id": "user5",
            "name": "정다은",
            "age": 27,
            "gender": "여성",
            "interests": ["요가", "명상", "반려동물"],
            "profile_text": "안녕하세요, 정다은입니다. 요가와 명상을 통해 마음의 평화를 찾고 있으며 강아지를 키우고 있습니다."
        }
    ]

def get_mock_questions() -> Dict[str, List[Dict[str, Any]]]:
    """사용자별 답변한 질문 목록 반환"""
    return {
        "user1": [
            {
                "id": "q1",
                "content": "당신의 인생에서 가장 중요한 가치는 무엇인가요?",
                "answer": "저에게 가장 중요한 가치는 자유입니다. 다양한 경험을 통해 성장하고 싶고, 새로운 도전을 두려워하지 않는 삶을 살고 싶습니다."
            },
            {
                "id": "q2",
                "content": "10년 후의 자신은 어떤 모습이길 바라나요?",
                "answer": "10년 후에는 여러 나라를 여행하며 다양한 문화를 경험한 사람이 되어있을 것 같습니다. 또한 제 꿈인 출판사를 운영하고 있을 것이라 생각합니다."
            },
            {
                "id": "q3",
                "content": "행복이란 무엇이라고 생각하시나요?",
                "answer": "행복은 매 순간을 충실하게 살며 자신의 선택에 만족하는 것이라고 생각합니다. 거창한 성취보다 소소한 일상의 기쁨을 느끼는 것이 진정한 행복이라고 생각해요."
            }
        ],
        "user2": [
            {
                "id": "q1",
                "content": "당신의 인생에서 가장 중요한 가치는 무엇인가요?",
                "answer": "성실함과 정직함이 가장 중요하다고 생각합니다. 어떤 상황에서도 최선을 다하고 정직하게 살아가는 것이 중요합니다."
            },
            {
                "id": "q4",
                "content": "가장 좋아하는 음악 장르는 무엇인가요?",
                "answer": "클래식 음악을 좋아합니다. 특히 쇼팽의 곡을 들으면 마음이 안정되고 영감을 받습니다. 취미로 피아노도 연주합니다."
            }
        ],
        "user3": [
            {
                "id": "q5",
                "content": "예술이 인생에 미치는 영향은 무엇인가요?",
                "answer": "예술은 제 인생의 큰 부분을 차지합니다. 그림을 그리면서 자신을 표현하는 방법을 배웠고, 다양한 감정과 생각을 캔버스에 담아내는 과정은 매우 치유적입니다."
            },
            {
                "id": "q6",
                "content": "가장 기억에 남는 여행지는 어디인가요?",
                "answer": "파리가 가장 기억에 남습니다. 예술의 도시라는 이름에 걸맞게 곳곳에 미술관과 갤러리가 있어 영감을 많이 받았고, 거리 자체가 하나의 예술 작품 같았어요."
            }
        ],
        "user4": [
            {
                "id": "q7",
                "content": "기술이 미래 사회에 미칠 영향은 무엇이라고 생각하나요?",
                "answer": "기술은 우리 삶을 더 편리하게 만들지만, 동시에 새로운 도전과 윤리적 문제를 가져올 것입니다. 특히 AI의 발전은 일자리 구조를 크게 바꿀 것이라 생각합니다."
            },
            {
                "id": "q8",
                "content": "일과 삶의 균형을 어떻게 유지하시나요?",
                "answer": "명확한 업무 시간을 설정하고 그 외 시간은 취미 활동이나 가족과 함께 보내려고 노력합니다. 주말에는 가능한 일 관련 생각을 피하고 테니스를 치러 가요."
            }
        ],
        "user5": [
            {
                "id": "q9",
                "content": "명상이 당신의 삶에 어떤 변화를 가져왔나요?",
                "answer": "명상을 시작한 후 스트레스가 크게 줄었고, 일상의 작은 일에 감사하는 마음을 갖게 되었습니다. 항상 바쁘게 살던 제가 잠시 멈춰 현재를 음미할 수 있게 되었어요."
            },
            {
                "id": "q10",
                "content": "반려동물과 함께하는 삶은 어떤가요?",
                "answer": "제 강아지 '코코'는 항상 저에게 무조건적인 사랑을 줍니다. 힘든 하루를 보내고 집에 돌아와도 반갑게 맞아주는 코코 덕분에 많은 위로를 받고 있어요."
            }
        ]
    }

def get_recommendations(message: str, count: int = 2) -> List[Dict[str, Any]]:
    """메시지를 바탕으로 추천 사용자 목록 반환"""
    # 실제 구현에서는 메시지 분석 및 사용자 매칭 등의 로직이 필요
    # 지금은 가상 데이터에서 랜덤하게 선택
    recommendations = get_mock_recommendations()
    return random.sample(recommendations, min(count, len(recommendations)))

def get_recommendation_profile(recommendation_id: str) -> Dict[str, Any]:
    """추천 사용자의 프로필 정보 반환"""
    recommendations = get_mock_recommendations()
    questions_by_user = get_mock_questions()
    
    # ID로 추천 정보 찾기
    recommendation = None
    for rec in recommendations:
        if rec["id"] == recommendation_id:
            recommendation = rec
            break
    
    if not recommendation:
        return {}
    
    # 사용자 질문/답변 찾기
    questions = questions_by_user.get(recommendation_id, [])
    
    # 전체 프로필 정보 구성
    return {
        **recommendation,
        "questions": questions
    } 