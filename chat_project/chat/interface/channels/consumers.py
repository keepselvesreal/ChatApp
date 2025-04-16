import json
import base64
import uuid
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ...infrastructure.state_management import ChatSystemState
from ...infrastructure.effect_executor import execute_effects
from ..flows import chat_flows
from ...utils import get_current_timestamp

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # 인증된 사용자는 그대로 사용하고, 익명 사용자는 UUID를 사용하여 고유한 ID 생성
        self.user_id = self.scope["user"].id if self.scope["user"].is_authenticated else f"user_{uuid.uuid4().hex[:8]}"
        self.room_group_name = f"chat_{base64.urlsafe_b64encode(self.room_name.encode()).decode()}"
        self.channel_name = self.channel_name
        
        # 연결 데이터 준비
        connection_data = {
            "roomName": self.room_name,
            "userId": self.user_id,
            "channelName": self.channel_name
        }
        
        # 연결 흐름 처리
        system_data, effects = chat_flows.handle_connection_flow(connection_data)
        
        # 상태 업데이트
        if system_data:
            current_state = ChatSystemState.get()
            ChatSystemState.commit(current_state, system_data)
        
        # 효과 실행
        for effect_type, *args in effects:
            if effect_type == "group_add":
                group_name, channel_name = args
                async_to_sync(self.channel_layer.group_add)(group_name, channel_name)
            elif effect_type == "group_send":
                group_name, message = args
                async_to_sync(self.channel_layer.group_send)(group_name, message)
            elif effect_type == "error":
                error_message = args[0]
                self.close(code=4000)
                return
        
        self.accept()
    
    def disconnect(self, close_code):
        # 연결 종료 데이터 준비
        connection_data = {
            "roomName": self.room_name,
            "userId": self.user_id,
            "channelName": self.channel_name
        }
        
        # 연결 종료 흐름 처리
        system_data, effects = chat_flows.handle_disconnection_flow(connection_data)
        
        # 상태 업데이트
        if system_data:
            current_state = ChatSystemState.get()
            ChatSystemState.commit(current_state, system_data)
        
        # 효과 실행
        for effect_type, *args in effects:
            if effect_type == "group_discard":
                group_name, channel_name = args
                async_to_sync(self.channel_layer.group_discard)(group_name, channel_name)
            elif effect_type == "group_send":
                group_name, message = args
                async_to_sync(self.channel_layer.group_send)(group_name, message)
    
    def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("message", "")
        
        # 메시지 처리 데이터 준비
        connection_data = {
            "roomName": self.room_name,
            "userId": self.user_id,
            "channelName": self.channel_name
        }
        
        # 메시지 처리 흐름
        system_data, effects = chat_flows.handle_message_flow(connection_data, content)
        
        # 상태 업데이트
        if system_data:
            current_state = ChatSystemState.get()
            ChatSystemState.commit(current_state, system_data)
        
        # 효과 실행
        for effect_type, *args in effects:
            if effect_type == "group_send":
                group_name, message = args
                async_to_sync(self.channel_layer.group_send)(group_name, message)
            elif effect_type == "send":
                channel_name, message = args
                if channel_name == self.channel_name:
                    self.send(text_data=json.dumps(message))
    
    # 채널 레이어 이벤트 핸들러
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["content"],
            "sender": event["sender_id"],
            "timestamp": event["timestamp"]
        }))
    
    def system_message(self, event):
        self.send(text_data=json.dumps({
            "type": "system_message",
            "message": event["content"],
            "sender": "system",
            "timestamp": event["timestamp"]
        }))
    
    def error_message(self, event):
        self.send(text_data=json.dumps({
            "type": "error",
            "message": event["content"],
            "sender": "system",
            "timestamp": event["timestamp"]
        })) 