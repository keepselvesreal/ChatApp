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