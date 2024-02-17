from rest_framework import serializers

from chat.models import Room, Message

class ListRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['sender', 'receiver']

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = []
        
        def validate(self, attrs):
            attrs = super().validate(attrs)
            attrs['sender'] = self.context['sender']
            attrs['receiver'] = self.context['receiver']
            return attrs

class ListMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['room', 'sender', 'message_text', 'created_at']

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_text', 'created_at']
        
        def validate(self, attrs):
            attrs = super().validate(attrs)
            attrs['room'] = self.context['room']
            attrs['sender'] = self.context['sender']
            return attrs
