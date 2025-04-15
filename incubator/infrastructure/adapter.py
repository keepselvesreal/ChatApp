from typing import Dict, Any
import json
import base64
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer

from interface.chat_system import ChatSystem
from application.validation import schema_validator

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """웹소켓 연결 처리"""
        # 연결 데이터 추출
        connection_data = self._extract_connection_data()
        
        # 채팅방 그룹에 참가 (Consumer의 핵심 책임)
        await self.channel_layer.group_add(
            connection_data["roomGroupName"],
            connection_data["channelName"]
        )
        
        # 웹소켓 연결 수락
        await self.accept()
        
        # 시스템에 연결 이벤트 처리 위임
        await ChatSystem.handle_connection(connection_data, self.channel_layer)

    async def disconnect(self, close_code):
        """웹소켓 연결 종료 처리"""
        # 연결 데이터 추출
        connection_data = self._extract_connection_data()
        
        # 채팅방 그룹에서 나가기 (Consumer의 핵심 책임)
        await self.channel_layer.group_discard(
            connection_data["roomGroupName"],
            connection_data["channelName"]
        )
        
        # 시스템에 연결 종료 이벤트 처리 위임
        await ChatSystem.handle_disconnection(connection_data, self.channel_layer)

    async def receive(self, text_data):
        """메시지 수신 처리"""
        # 연결 데이터 추출
        connection_data = self._extract_connection_data()
        
        # 메시지 데이터 처리
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get('message', '')
        
        # 시스템에 메시지 처리 위임
        try:
            await ChatSystem.handle_message(connection_data, message_content, self.channel_layer)
        except ValueError as e:
            print(f"Error processing message: {e}")

    async def chat_message(self, event):
        """채팅 메시지 이벤트 처리"""
        try:
            # 메시지 유효성 검증
            if not schema_validator.validate_message(event):
                return
            
            # 클라이언트로 메시지 전송
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
        
        # user_id가 없으면 생성
        if not hasattr(self, 'user_id'):
            self.user_id = str(uuid.uuid4())[:8]
        
        return {
            "roomName": room_name,
            "roomGroupName": room_group_name,
            "userId": self.user_id,
            "channelName": self.channel_name
        }