from typing import Dict, Any
import json
import base64
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer

from ..interface.chat_system import ChatSystem


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """웹소켓 연결 처리"""
        connection_data = self._extract_connection_data()
        
        await self.channel_layer.group_add(
            connection_data["roomGroupName"],
            connection_data["channelName"]
        )
        
        await self.accept()
        await ChatSystem.handle_connection(connection_data, self.channel_layer)

    async def disconnect(self, close_code):
        """웹소켓 연결 종료 처리"""
        connection_data = self._extract_connection_data()
        
        await self.channel_layer.group_discard(
            connection_data["roomGroupName"],
            connection_data["channelName"]
        )
        
        await ChatSystem.handle_disconnection(connection_data, self.channel_layer)

    async def receive(self, text_data):
        """메시지 수신 처리"""
        connection_data = self._extract_connection_data()
        
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json.get('message', '')
            await ChatSystem.handle_message(connection_data, message_content, self.channel_layer)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except ValueError as e:
            print(f"Error processing message: {e}")

    async def chat_message(self, event):
        """채팅 메시지 이벤트 처리"""
        try:
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'userId': event['userId']
            }))
        except Exception as e:
            print(f"Error in chat_message: {e}")

    def _extract_connection_data(self) -> Dict[str, Any]:
        """웹소켓 연결 정보 추출"""
        room_name = self.scope['url_route']['kwargs']['room_name']
        room_group_name = base64.urlsafe_b64encode(room_name.encode()).decode()
        
        if not hasattr(self, 'user_id'):
            self.user_id = str(uuid.uuid4())[:8]
        
        return {
            "roomName": room_name,
            "roomGroupName": room_group_name,
            "userId": self.user_id,
            "channelName": self.channel_name
        }