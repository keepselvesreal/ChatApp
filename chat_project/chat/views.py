from django.shortcuts import render, redirect
from .models import ChatRoom

def index(request):
    # 채팅방 목록 조회
    rooms = ChatRoom.objects.all().order_by('-created_at')
    
    # 새 채팅방 생성 처리
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            # 새 채팅방 생성 또는 기존 채팅방 가져오기
            ChatRoom.objects.get_or_create(name=room_name)
            return redirect('chat:room', room_name=room_name)
    
    return render(request, 'chat/index.html', {'rooms': rooms})

def room(request, room_name):
    # 채팅방 접속 시 채팅방이 없으면 생성
    ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def question(request):
    # 오늘의 질문 페이지 - taste_finder 앱으로 리다이렉트
    return redirect('/taste/question/')

def fortune(request):
    # 운명 찾기 페이지 - destiny_finder 앱으로 리다이렉트
    return redirect('/destiny/')