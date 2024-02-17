from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt

from chat.serializers import CreateRoomSerializer, CreateMessageSerializer, ListRoomSerializer, ListMessageSerializer

from chat.models import Room, Message
from users.models import User

'''Список чатов у пользователя'''
class ListChatsAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")
        
        user = get_object_or_404(User, email=payload['id'])
        
        try:
            chat_room = (Room.objects.filter(sender=user) | Room.objects.filter(receiver=user))
        except:
            raise Http404('Чаты не найдены!')
        
        serializer = ListRoomSerializer(chat_room, many=True)
        return Response(serializer.data)

'''Диалог пользователя с другим пользователем'''
class DialogAPIView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Вы не авторизованы!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Вы не авторизованы!")
        
        room = Room.objects.filter(pk=pk).first()
        
        if not (payload['id'] == room.sender.email or payload['id'] == room.receiver.email):
            raise AuthenticationFailed('Вы не состоите в этом чате!')
        
        messages = Message.objects.filter(room=pk).order_by('-created_at')

        serializer = ListMessageSerializer(messages, many=True)
        return Response(serializer.data)
