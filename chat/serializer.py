from rest_framework import serializer

from chat.models import Room, Message

class RoomSerializer(serializer.ModelSerializer):
    class Meta:
        model = Room
        fields = ['client', 'master']
        
class MessageSerializer(serializer.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_text', 'created_at']
        
        def validate(self, attrs):
            attrs = super().validate(attrs)
            attrs['room'] = self.context['room']
            return attrs
