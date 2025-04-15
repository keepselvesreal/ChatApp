import json
import uuid
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = base64.urlsafe_b64encode(self.room_name.encode()).decode()
        self.user_id = str(uuid.uuid4())[:8]
        
        # 채팅방 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # 웹소켓 연결 수락
        await self.accept()
        
        # 사용자 입장 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user_id}님이 입장했습니다.',
                'user_id': 'system'
            }
        )

    async def disconnect(self, close_code):
        # 채팅방 그룹에서 제거
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # 사용자 퇴장 메시지 전송 (try-except로 감싸서 오류 방지)
        try:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.user_id}님이 퇴장했습니다.',
                    'user_id': 'system'
                }
            )
        except Exception:
            pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # 그룹에 메시지 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': self.user_id
                }
            )
        except Exception as e:
            # 오류 발생 시 로그 출력
            print(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        # WebSocket으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id']
        }))