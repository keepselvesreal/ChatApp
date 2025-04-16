from django.test import TestCase, Client
from django.urls import reverse
import json

class DestinyFinderViewTests(TestCase):
    def test_destiny_chat_page_loads(self):
        response = self.client.get(reverse('destiny_finder:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '운명 찾기')
    
    def test_chat_with_llm_returns_response(self):
        client = Client()
        
        # 채팅 메시지 전송
        response = client.post(
            reverse('destiny_finder:send_message'),
            json.dumps({'message': '나에게 맞는 사람은 어떤 사람인가요?'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('response', data)
        self.assertTrue(len(data['response']) > 0)
    
    def test_chat_history_persists(self):
        client = Client()
        
        # 첫 번째 메시지 전송
        client.post(
            reverse('destiny_finder:send_message'),
            json.dumps({'message': '나는 어떤 사람과 잘 맞을까요?'}),
            content_type='application/json'
        )
        
        # 두 번째 메시지 전송
        client.post(
            reverse('destiny_finder:send_message'),
            json.dumps({'message': '더 자세히 알려줄래요?'}),
            content_type='application/json'
        )
        
        # 대화 내역 조회
        response = client.get(reverse('destiny_finder:chat_history'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data['messages']), 4)  # 사용자 2개 + LLM 응답 2개
        
    def test_llm_response_includes_recommended_users(self):
        """LLM 응답에 추천 사용자 목록이 포함되는지 테스트"""
        client = Client()
        
        # 메시지 전송
        response = client.post(
            reverse('destiny_finder:send_message'),
            json.dumps({'message': '나에게 맞는 사람을 추천해줘'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # 응답에 추천 사용자 정보가 포함되어 있어야 함
        self.assertIn('recommended_users', data)
        self.assertTrue(len(data['recommended_users']) > 0)
        
        # 추천 사용자는 id와 name을 가져야 함
        recommended_user = data['recommended_users'][0]
        self.assertIn('id', recommended_user)
        self.assertIn('name', recommended_user)
    
    def test_get_recommendation_profile(self):
        """추천 사용자 프로필 정보 조회 테스트"""
        client = Client()
        
        # 임의의 사용자 ID로 프로필 정보 요청
        response = client.get(
            reverse('destiny_finder:get_recommendation_profile', args=['user1'])
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # 프로필 정보 검증
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('age', data)
        self.assertIn('gender', data)
        self.assertIn('interests', data)
        self.assertIn('profile_text', data)
        self.assertIn('questions', data)
        
        # 질문 및 답변 정보 검증
        self.assertTrue(len(data['questions']) > 0)
        question = data['questions'][0]
        self.assertIn('id', question)
        self.assertIn('content', question)
        self.assertIn('answer', question) 